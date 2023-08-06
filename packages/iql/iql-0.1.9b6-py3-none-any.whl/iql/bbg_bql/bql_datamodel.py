# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import re
from typing import Dict, List, Optional, Union, Tuple
import pandas as pd
import itertools
import copy
from dataclasses import dataclass, field
from iql.bbg_bql.bql_wrapper import (
    BaseBqlQuery,
    security_to_finalstr,
    construct_bql_query,
    execute_bql_str_list_async_q,
)

logger = logging.getLogger(__name__)

SECURITY_KEYWORD = "$SECURITY"


@dataclass
class RawBqlQuery(BaseBqlQuery):
    """A full BQL query. Ideally, use $SECURITY instead of a single equity name"""

    fieldpattern = re.compile(r"(?s).*get\s*\((.*?)\)\s*for.*")

    bql_query_string: str
    security: Optional[str] = None
    params: Dict = field(
        default_factory=dict
    )  # parameters. Convention is $FIELD: value

    def get_fields(self) -> List[str]:
        """Extracts individual fields from the BQL get statement.
        TODO: Handle unbalanced escaped/quoted parens"""

        query = self.to_bql_query()
        match = self.fieldpattern.fullmatch(query)

        if match is None:
            raise ValueError(f"Couldn't extract GET from: {query}")

        else:
            getclause = match.group(1)
            fields = []
            start = 0
            depth = 1
            for i in range(len(getclause)):
                c = getclause[i]
                if c == "," and depth == 1:
                    fields.append(getclause[start:i].strip())
                    start = i + 1
                if c == "(":
                    depth += 1
                if c == ")":
                    depth -= 1

            fields.append(getclause[start:].strip())

        return fields

    def to_bql_query(self) -> str:
        if self.security is not None:
            new_str = self.bql_query_string.replace(SECURITY_KEYWORD, self.security)
        else:
            new_str = self.bql_query_string

        for param, value in self.params.items():
            new_str = new_str.replace(param, value)

        logger.debug(f"Raw query to string: {new_str}")

        if "preferences" not in new_str:
            logger.debug("Adding default preferences")
            new_str += " \n preferences(addcols=all)"
        return new_str


@dataclass
class BqlQuery(BaseBqlQuery):
    name: str
    fields: list

    security: Union[str, list]
    let_str: Optional[str]
    with_params: Optional[str]

    for_str: str = SECURITY_KEYWORD
    params: Dict = field(
        default_factory=dict
    )  # parameters. Convention is $FIELD: value

    def get_fields(self) -> List[str]:
        return self.fields

    def to_bql_query(self) -> str:
        for_str_mod = security_to_finalstr(self.for_str)

        if SECURITY_KEYWORD not in self.params and self.security is not None:
            self.params[SECURITY_KEYWORD] = self.security

        sec = self.params.get(SECURITY_KEYWORD)
        if self.let_str is not None and sec is not None:
            let_str_mod = self.let_str.replace(SECURITY_KEYWORD, sec)
        else:
            let_str_mod = None
        query_str = construct_bql_query(
            self.fields, for_str_mod, self.with_params, let_str_mod
        )

        logger.debug(f"After construction but before replacement: {query_str}")
        for param, value in self.params.items():
            if param == SECURITY_KEYWORD:
                if isinstance(value, str) and (
                    "'" in self.for_str or "(" in self.for_str or "[" in self.for_str
                ):
                    # Don't change anything if security is a list, or the for_str is a formula
                    pass
                else:
                    value = security_to_finalstr(self.params[SECURITY_KEYWORD])

            query_str = query_str.replace(param, value)

        logger.debug(f"BQL Query to String: {query_str}")
        return query_str


class DateGen:
    start_date: str
    end_date: str
    date_param: str
    date_frequency: str
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    # MS = Month Begin
    # QS = Quarter Begin

    def __init__(self, date_param, start_date, end_date, date_frequency="MS"):
        self.date_param = date_param
        self.start_date = start_date
        self.end_date = end_date
        self.date_frequency = date_frequency

    def __iter__(self):
        data = (
            pd.date_range(self.start_date, self.end_date, freq=self.date_frequency)
            .strftime("%Y-%m-%d")  # type: ignore
            .tolist()
        )

        result = list(zip(itertools.repeat(self.date_param), data))

        return iter(result)


class UniqueColIter:
    dataframe: pd.DataFrame
    id_col: str  # column in the dataframe
    id_param: str  # param name to pass to next query

    def __init__(self, id_col, id_param, dataframe):
        self.dataframe = dataframe
        self.id_col = id_col
        self.id_param = id_param

    def __call__(self):
        pass

    def __iter__(self):
        if self.id_col not in self.dataframe.columns:
            raise ValueError(
                f"{self.id_col} not in dataframe, columns = {self.dataframe.columns}"
            )

        data = self.dataframe[self.id_col].unique()

        result = list(zip(itertools.repeat(self.id_param), data))

        return iter(result)


@dataclass
class _PipelineBqlQuery:
    query: BaseBqlQuery

    copy_from_previous: Optional[
        Tuple[str, str]
    ] = None  # (df column name, parameter name)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date_param: Optional[str] = None
    date_frequency: Optional[str] = None

    def execute(self, previousQuery: Optional[BaseBqlQuery]) -> bool:
        generators = []
        if self.date_param is not None:
            assert self.start_date is not None and self.end_date is not None
            generators.append(DateGen(self.date_param, self.start_date, self.end_date))
        if self.copy_from_previous is not None:
            if previousQuery is None or previousQuery.to_df() is None:
                raise ValueError(
                    "Unexpected, copy_from_previous defined, but previousQuery or previousQuery.dataframe is None"
                )

            parent_dataframe = previousQuery.to_df()
            id_col = self.copy_from_previous[0]
            param_name = self.copy_from_previous[1]

            logger.info(UniqueColIter(id_col, param_name, parent_dataframe).__iter__())

            generators.append(UniqueColIter(id_col, param_name, parent_dataframe))

        if len(generators) == 0:
            # No generators, just execute
            return self.query.execute()
        else:
            queries = []

            logger.info("Generating queries")
            # Create the queries
            for resultparams in itertools.product(*generators):
                # resultparams is a iterator of Tuples (from the generators)
                logger.info(f"Running with parameters: {resultparams}")
                for param, value in resultparams:
                    if self.query.params is not None:
                        self.query.params[param] = value

                # self.params[date_param] = date_value # pass the date to this query
                query_copy = copy.deepcopy(self.query)

                queries.append(query_copy)

            logger.info("Done generating queries, executing")
            # execute the queries
            execute_bql_str_list_async_q(queries)
            logger.info("Done executing, assembling")

            dfs = []
            last_execution_status = BaseBqlQuery.STATUS_FAILURE
            for q in queries:
                last_execution_status = q.execution_status
                if last_execution_status != BaseBqlQuery.STATUS_COMPLETED:
                    logger.info(f"Query failed, stopping execution. {q.exception_msg}")
                    return False

                qdf = q.to_df()
                for param_key, value in q.params.items():
                    if isinstance(value, list) and len(value) == 1:
                        value = value[0]
                    param = param_key.replace("$", "") + "_PARAM"
                    qdf[param] = value

                dfs.append(qdf)

            self.query._df = pd.concat(dfs)
            self.query._df.reset_index(drop=True, inplace=True)
            self.query.execution_status = last_execution_status

        return True


@dataclass
class QueryPipeline:
    queries: List[_PipelineBqlQuery] = field(default_factory=list)

    def add_query(
        self,
        query: BaseBqlQuery,
        copy_from_previous: Optional[Tuple[str, str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_param: Optional[str] = None,
        date_frequency: str = "MS",
    ):
        pq = _PipelineBqlQuery(
            query=query,
            copy_from_previous=copy_from_previous,
            start_date=start_date,
            end_date=end_date,
            date_param=date_param,
            date_frequency=date_frequency,
        )
        self.queries.append(pq)

    def execute(self):
        previousQuery: Optional[BaseBqlQuery] = None

        for query in self.queries:
            success = query.execute(previousQuery)

            previousQuery = query.query

            if not success:
                logger.warning(f"Failure executing previousQuery {previousQuery}")
                return False

        # everything passed
        assert previousQuery is not None and previousQuery.to_df() is not None
        logger.debug("Pipeline execution passed successfully")
        return True

    def successful(self) -> bool:
        success = (
            self.queries[-1].query.execution_status == BaseBqlQuery.STATUS_COMPLETED
        )
        if not success:
            logger.warning(f"Failure: {self.queries[-1].query.exception_msg}")
        return success

    def dataframe(self) -> Optional[pd.DataFrame]:
        return self.queries[-1].query.to_df()

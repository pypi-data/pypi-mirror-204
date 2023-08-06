# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import re
from pandas import DataFrame
from typing import List, Optional, Dict
from dataclasses import dataclass, field

from iql import q_cache
from iql.bbg_bql.bql_wrapper import BaseBqlQuery, execute_bql_str_list_async_q
from iql.bbg_bql.bql_datamodel import RawBqlQuery
from iql.iqmoql import (
    IqlExtension,
    register_extension,
    SubQuery,
    get_subqueries_flat,
    IqlQueryContainer,
)


logger = logging.getLogger(__name__)

_KEYWORD = "bql"

_bql_start_pattern = r"(?si)\(\s*((get)|(let))\s*\("
_bql_pat = re.compile(_bql_start_pattern)

_QUERY_FOR_PATTERN = re.compile(
    r"(?s)(.*for\s*\((.*?)\)\s*)((with.*?)?)\s*((preferences.*)?)"
)


@dataclass
class _IqmoBqlQuery(SubQuery):
    # Extended BQL language to add "iqmo" options
    # such as "splitid" and pivoting
    # Syntax; pivot(id, name)
    # Syntax 2: pivot([id:col2], name)
    bqlquery: BaseBqlQuery = field(init=False)

    # detects everything before "(.*) as #..."

    def validate_fix_column_names(self, df) -> DataFrame:
        # BQL does two annoying things:
        # 1. It drops duplicate columns silently, even if the duplicates are desired or slightly different.
        # This detects this case, and throws an exception to force the query writer to handle it.
        # 2. It sometimes ignores the "alias", so this will re-insert the alias if needed

        if len(df) == 0:
            return df

        cols_returned = list(df["name"].unique())
        cols_expected = self.bqlquery.get_fields()
        if len(cols_returned) != len(cols_expected):
            raise ValueError(
                f"""Unexpected number of columns returned. Expected {len(cols_expected)}, 
                got {len(cols_returned)}. Got: {df['name'].unique()}, expected {cols_expected}"""
            )

        if (
            True
        ):  # We expect that the columns match 1 to 1, so make sure the columns match the "as" of cols_expected
            for i in range(len(cols_returned)):
                r = cols_returned[i]
                e = cols_expected[i]

                if r == e or re.sub(r"\s+", "", r) == e:
                    # it's equal, or without spaces, it's equal
                    continue

                if r[0] == "#":
                    # this is an aliased field
                    continue

                raise ValueError(f"Expected {e}, got {r}")

        return df

    def execute(self) -> bool:
        # populate_from_cache is called from execute_batch, doesn't need to be run again here
        if self.dataframe is not None:
            return True

        success = self.execute_internal()

        if success:
            df = self.bqlquery.to_df()

            df = self.extension.apply_pandas_operations_prepivot(df, self.options)

            df = self.extension.pivot(df, self.options.get("pivot"))  # type: ignore
            df = self.extension.apply_pandas_operations_postpivot(df, self.options)

            self.dataframe = df
            self.save_to_cache()

            return success
        else:
            allow_failure_opt = self.options.get("allow_failure")
            if allow_failure_opt is None or (
                isinstance(allow_failure_opt, bool) and allow_failure_opt is False
            ):
                return False
            else:
                if isinstance(allow_failure_opt, bool) and allow_failure_opt is True:
                    logger.info(
                        "Query failed, but allow_failure is enabled. Creating an empty dataframe with one id column."
                    )
                    self.dataframe = DataFrame(columns=["id"])
                else:
                    if isinstance(allow_failure_opt, str):
                        cols: List[str] = [allow_failure_opt]
                    else:
                        cols: List[str] = allow_failure_opt  # type: ignore
                    logger.info(
                        f"Query failed, but allow_failure is enabled. Creating an empty dataframe with cols = {cols}"
                    )

                    self.dataframe = DataFrame(columns=cols)
                return True

    def execute_internal(self) -> bool:
        if self.bqlquery.execution_status == BaseBqlQuery.STATUS_FAILURE:
            return False

        if self.bqlquery.execution_status == BaseBqlQuery.STATUS_COMPLETED:
            return True

        working_df = None

        # If it already ran, don't run again
        if not self.bqlquery.execution_status == BaseBqlQuery.STATUS_COMPLETED:
            # logger.info("Not splitting")
            success = self.bqlquery.execute()

            if not success:
                logger.debug(f"Result {success}")
                return False

        # query has passed
        if working_df is None:
            working_df = self.bqlquery.to_df()

        assert working_df is not None

        # validate column names: disabled for now, still a work in progress
        # working_df = self.validate_fix_column_names(working_df)
        self.dataframe = working_df
        return True


@dataclass
class BqlExtension(IqlExtension):
    def create_subquery(
        self, subquery: str, name: str, iqc: IqlQueryContainer
    ) -> SubQuery:
        iq = _IqmoBqlQuery(subquery=subquery, name=name, extension=self, iqc=iqc)

        bqlstr = iq.get_query()
        q = RawBqlQuery(bqlstr)
        iq.bqlquery = q
        return iq

    def create_subqueries(
        self,
        query: str,
        name: str,
        iqc: IqlQueryContainer,
        create_function: object = None,
    ) -> List["SubQuery"]:
        return super().create_subqueries(
            query=query, name=name, iqc=iqc, create_function=self.create_subquery
        )

    def execute_batch(self, subqueries: List[_IqmoBqlQuery]) -> Dict[str, DataFrame]:
        # Caching operates at two levels here:
        # The SubQuery result, and within the bql_wrapper
        # To force a refresh, we'll clear both the subquery and bql raw query
        # cache

        subqueries_flat: List[_IqmoBqlQuery] = get_subqueries_flat(subqueries)  # type: ignore

        for sq in subqueries_flat:
            sq.populate_from_cache()

        clear_inner_caches = False

        needs_to_be_cleared = [q for q in subqueries_flat if clear_inner_caches]
        logger.debug(f"Clearing {len(needs_to_be_cleared)}")
        # clear lower-level cache entries
        for q in needs_to_be_cleared:
            q_cache.clear(q.bqlquery.to_bql_query())

        to_run: List[_IqmoBqlQuery] = [
            sq for sq in subqueries_flat if sq.dataframe is None
        ]

        queries = [q.bqlquery for q in to_run]

        # We already checked whether its cached AND whether caching is allowed in sq.populate_from_cache
        logger.debug(f"Executing {len(queries)}")
        execute_bql_str_list_async_q(queries)

        # Then update the subqueries
        for q in subqueries_flat:
            if q.bqlquery.execution_status == BaseBqlQuery.STATUS_FAILURE:
                if q.options.get("allow_failure") is None:
                    raise ValueError(
                        f"BQL SubQuery failed {q.bqlquery.exception_msg}: {q.bqlquery.to_bql_query()} {q.options}"
                    )
            q.execute()

        completed_dfs = {}
        # Final step to merge any grouped subqueries.
        for q in subqueries:
            q.merge()
            df = q.dataframe
            completed_dfs[q.name] = df

        return completed_dfs


def execute_bql(query: str, pivot: Optional[str] = None) -> DataFrame:
    """Convenience function for testing, or executing single queries"""

    if _KEYWORD in query:
        raise ValueError(f"Pass raw BQL queries only, don't wrap with {_KEYWORD}(...)")

    elif pivot is not None:
        suffix = f", pivot={pivot}"

    else:
        suffix = ""

    query = f'{_KEYWORD}("{query}"{suffix})'
    extension = BqlExtension(_KEYWORD)

    logger.debug(f"Converted to: {query}")
    sqs = extension.create_subqueries(query, "Anon", iqc=None)  # type: ignore
    sq = sqs[0]

    sq.execute()  # type: ignore

    if sq.dataframe is None:
        raise ValueError(f"Unable to execute {sq.subquery}")

    return sq.dataframe


def execute_bql_batch(queries: List[str]) -> Dict[str, Optional[DataFrame]]:
    """Batch executes multiple BQL Queries. Much faster than running serially."""
    extension = BqlExtension(_KEYWORD)

    wrapped_queries = [f'{_KEYWORD}("{q}")' for q in queries]

    iqs = []
    for query in wrapped_queries:
        sqs = extension.create_subqueries(query, "Anon", iqc=None)  # type: ignore
        iqs.extend(sqs)

    extension.execute_batch(iqs)

    return {sq.subquery: sq.dataframe for sq in iqs}


def register(keyword: str):
    global _KEYWORD
    _KEYWORD = keyword
    extension = BqlExtension(keyword=keyword)
    register_extension(extension)

# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import sqlparse
import importlib
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple, Callable
from pandas import DataFrame
from pyarrow import Table
import pandas as pd
from abc import abstractmethod
from iql import q_cache as qc
from iql import options_parser
from iql import threading_experimental as te


# Cache Settings
# Use iqmoql.activate_cache() before first execute() to
# ensure settings propogate to individual extensions.
# Infinite in memory cache by default
_CACHE_PERIOD = -1
_USE_FILE_CACHE = False
DEFAULT_EXT_DIRECTORY = None

# DB_MODULE is loaded on first call to get_dbmodule()
# Replace this string with another connector prior to first use,
# or set _DBCONNECTOR to None after changing.
DB_MODULE: str = "iql.db_connectors.duckdb_connector"

_EXTENSIONS: Dict[Tuple[str, str], "IqlExtension"] = {}
_DBCONNECTOR: Optional["IqlDatabaseConnector"] = None

# Used internally to name the dataframes
_DFPREFIX: str = "iqldf"

# Add extensions via register_extension()
# Extensions are loaded on first access, to avoid requiring
# unused dependencies
_KNOWN_EXTENSIONS: Dict[str, str] = {
    "bql": "iql.bbg_bql.bql_extension",
    "s3": "iql.extensions.aws_s3_extension",
    "fred": "iql.extensions.fred_extension",
    "kaggle": "iql.extensions.kaggle_extension",
    "edgar": "iql.extensions.edgar_extension",
    "pandas": "iql.extensions.pandas_extension",
}

_ALIASES: Dict[str, str] = {}

logger = logging.getLogger(__name__)


def _find_closing_paren(text: str, start: int) -> int:
    # TODO: Handle escaping
    paren_depth = 1
    quote_stack = []
    for i in range(start, len(text)):
        c = text[i]
        if c == "(" and len(quote_stack) == 0:
            paren_depth += 1
        elif c == "'" or c == '"':
            if len(quote_stack) == 0:
                quote_stack.append(c)
            elif quote_stack[len(quote_stack) - 1] == c:
                quote_stack.remove(c)
        elif c == ")" and len(quote_stack) == 0:
            paren_depth -= 1

        if paren_depth == 0:
            end = i
            return end
    raise ValueError("Never found closing parenthesis, probably unbalanced query")


def get_keyword_list(keywords: Optional[List[str]] = None) -> str:
    if keywords is None:
        keywords = list(_KNOWN_EXTENSIONS.keys())
    _keyword_list = "|".join((k if isinstance(k, str) else k[0] for k in keywords))
    return _keyword_list


def _extract_subquery_strings(
    query, keywords: Optional[List[str]] = None
) -> List[Tuple[str, str, str, str]]:
    global _cached_pats
    """Finds the subqueries start with keyword, along with matching end paren
    keyword(....)
    keyword.subword(....)
    """
    _keyword_list = get_keyword_list(keywords)

    _kpat = re.compile(rf"(?s)({_keyword_list})(\.(\w+))?\s*\(")

    results = []
    for m in re.finditer(_kpat, query):
        keyword = m.group(1)
        subword = m.group(3)
        paren_start = m.end()  # just after the last paren

        paren_end = _find_closing_paren(query, paren_start)

        outer = query[m.start() : paren_end + 1]
        inner = query[paren_start : paren_end + 1]
        logger.debug(
            f"Extracted subquery: {keyword}.{subword} at {paren_start}:{paren_end}"
        )

        results.append((keyword, subword, outer, inner))

    return results


def rename_dupe_arrow_columns(pat: Table) -> Table:
    # PyArrow can't export to Pandas if there are duplicate columns
    cols = pat.column_names
    unique_cols = set(cols)

    if len(unique_cols) == len(cols):
        # everything is unique
        return pat
    else:
        newcols = []
        print(f"Has dupes, {cols}")
        seen = set()
        for col in cols:
            if col not in seen:
                seen.add(col)
                newcols.append(col)
            else:
                idx = 1
                while (newcol := f"{col}_{idx}") in seen or newcol in unique_cols:
                    idx += 1
                newcols.append(newcol)

        pat = pat.rename_columns(newcols)

        return pat


@dataclass
class IqlResult:
    _table: Table

    def arrow(self):
        return self._table

    def df_numpy(self):
        return self._table.to_pandas()

    def df_arrow(self):
        return self._table.to_pandas(types_mapper=pd.ArrowDtype)


class IqlDatabase:
    @abstractmethod
    def execute_query(
        self, query: str, completed_dfs: Dict[str, DataFrame]
    ) -> Optional[IqlResult]:
        raise ValueError("Implement Me")

    @abstractmethod
    def get_connection(self) -> object:
        raise ValueError("Implement Me")

    @abstractmethod
    def close_db(self):
        raise ValueError("Implement Me")


class IqlDatabaseConnector:
    @abstractmethod
    def create_database(self) -> IqlDatabase:
        raise ValueError("Implement Me")

    @abstractmethod
    def create_database_from_con(self, con: object) -> IqlDatabase:
        raise ValueError("Implement Me")


_lasttoken = None


def get_subqueries_flat(queries: List["SubQuery"]) -> List["SubQuery"]:
    subqueries_flat = [
        q_inner for q_outer in queries for q_inner in q_outer.get_subqueries_flat()
    ]
    return subqueries_flat


@dataclass
class IqlExtension:
    keyword: str
    subword: str = field(default=None, init=True)  # type: ignore

    # Extensions must be parallelizable, or must
    # implement their own execute_batch.
    # Can only contain pickleable elements
    # etc

    # Determines whether the local cache settings should be used
    # vs  CACHE_PERIOD and
    # USE_FILE_CACHE
    use_default_caching: bool = field(default=True, init=False)
    _cache_period: Optional[int] = field(default=None, init=False)
    _use_file_cache: bool = field(default=False, init=False)
    temp_file_directory: Optional[str] = field(default=None, init=False)

    def get_output_dir(self) -> str:
        tempdir = (
            self.temp_file_directory if self.temp_file_directory is not None else "./"
        )
        return tempdir

    def allow_cache_read(self, sq: "SubQuery") -> bool:
        """Dont use cached values"""
        if sq.options.get("nocache") is True:
            return False
        elif sq.options.get("cache") is not None:
            return True
        elif self.get_cache_period() is None:
            return False
        else:
            return True

    def allow_cache_save(self, sq: "SubQuery") -> bool:
        return self.allow_cache_read(sq)

    def get_cache_period(self) -> Optional[int]:
        if self.use_default_caching:
            return _CACHE_PERIOD
        else:
            return self._cache_period

    def use_file_cache(self) -> bool:
        if self.use_default_caching:
            return _USE_FILE_CACHE
        else:
            return self._use_file_cache

    def use_path_replacement(self) -> bool:
        """Some extensions just return a filestring to use instead of the SubQuery, such as the
        S3 Extension. If execute() returns None, then use_path_replacement must be used.
        """
        return False

    def get_path_replacement(
        self, subquery: "SubQuery", quote: bool = True
    ) -> Optional[str]:
        """Quoting is done here, with the expectation that some path replacements might actually be function calls."""
        tempdir = self.get_output_dir()
        filepath = f"{tempdir}/{subquery.name}.parquet"

        if quote:
            outpath = f"'{filepath}'"
        else:
            outpath = filepath

        logger.info(f"Converted {subquery} to {outpath}")
        return outpath

        """Used for extensions which use a native duckdb extension to access the underlying data"""
        return None

    @abstractmethod
    def executeimpl(self, sq: "SubQuery") -> Optional[DataFrame]:
        raise ValueError("Implement Me")

    def execute(self, sq: "SubQuery") -> Optional[DataFrame]:
        # usage: select * from (verityapi(functionname, targetname)) as verityquery
        # An empty response means no response was needed
        # Internal failure must raise an exception
        if sq.populate_from_cache() and sq.dataframe is not None:
            return sq.dataframe

        logger.debug(f"Executing query {sq.subquery}")

        df = self.executeimpl(sq)

        if df is None and not self.use_path_replacement():
            raise ValueError("Empty DF, should never reach here")
        else:
            if df is not None:
                pivot_options = sq.options.get("pivot")
                melt_options = sq.options.get("melt")

                df = self.apply_pandas_operations_prepivot(df, sq.options)

                if pivot_options is not None:
                    df = self.pivot(df, pivot_options)  # type: ignore
                if melt_options is not None:
                    df = df.melt(melt_options)

                df = self.apply_pandas_operations_postpivot(df, sq.options)

                sq.dataframe = df

                sq.save_to_cache()

                return df

    def execute_batch(self, queries: List["SubQuery"]) -> Dict[str, DataFrame]:
        """Default implementation runs individually, override for functions that can be batched, such as
        BQL's _many functions.
        Executes all subqueries first, then merges as required.
        SubQueries are executed in a threadpool, which has minimal benefit."""

        completed_dfs = {}
        # context = get_context('spawn')

        subqueries_flat = get_subqueries_flat(queries)
        # Get all the queries (and any queries inside SubQueryGroups)

        # Executes the ungrouped queries

        if te.ENABLED and te.MAX_PROCESSES > 1 and len(queries) > 1:
            te.execute_batch(subqueries_flat, self.execute)
        else:
            for query in subqueries_flat:
                self.execute(query)  # type: ignore

        completed_dfs = {}
        # Merge the results
        for query in queries:
            # For single subqueries, this is a noop
            # For subquery groups, this merges the results of the children
            query.merge()

            df = query.dataframe
            if df is None and not self.use_path_replacement():
                raise ValueError(f"Empty DF, {query.get_query()} failed")
            elif df is None:
                logger.debug("Using path replacement, no DF")
            else:
                query.dataframe = df  # type: ignore
                completed_dfs[query.name] = df

        return completed_dfs

    def create_subquery(
        self, subquery: str, name: str, iqc: "IqlQueryContainer"
    ) -> "SubQuery":
        logger.debug("Creating subquery")
        sq = SubQuery(extension=self, subquery=subquery, name=name, iqc=iqc)
        return sq

    def create_subqueries(
        self,
        query: str,
        name: str,
        iqc: "IqlQueryContainer",
        create_function: Optional[Callable] = None,
    ) -> List["SubQuery"]:
        """Converted to always return a single item, but left logic in place to support multiple"""
        logger.debug(f"Creating a subquery {name} for {query}")

        if create_function is None:
            create_function = self.create_subquery

        sq = create_function(subquery=query, name=name, iqc=iqc)

        # If a paramlist is passed, create one subquery for each value

        if "paramquery" in sq.options:
            paramquery: Tuple[str, str] = sq.options.get("paramquery")  # type: ignore

            if (
                len(paramquery) == 2
                and isinstance(paramquery[0], str)
                and isinstance(paramquery[1], str)
            ):
                parameter_name = paramquery[0]
                param_query = paramquery[1]
                result = iqc.db.execute_query(param_query, completed_dfs={})  # type: ignore

                df = result.df_numpy()
                parameter_values = df[df.columns[0]].values
                logger.debug(f"Values {parameter_values}")
            else:
                raise ValueError(f"Invalid options passed to paramquery: {paramquery}")

        elif "paramlist" in sq.options:
            paramlist: Tuple[str, List[str]] = sq.options.get("paramlist")  # type: ignore

            if not isinstance(paramlist, list) and len(paramlist) != 2:
                raise ValueError("paramlist must be a Tuple of (param, [values])")

            parameter_name = paramlist[0]
            parameter_values: List[str] = paramlist[1]
            logger.debug(f"Found paramlist: {parameter_name} => {parameter_values}")

            if parameter_values is None or len(parameter_values) == 0:
                raise ValueError("Empty values passed to paramlist passed")

            if isinstance(parameter_values, str):
                parameter_values = [parameter_values]
        else:
            parameter_name = None
            parameter_values = None  # type: ignore

        if parameter_name is not None:
            assert parameter_values is not None and len(parameter_values) > 0
            sqs: List["SubQuery"] = []
            count = 1

            for v in parameter_values:
                v_query = query.replace(parameter_name, v)

                sq = create_function(  # type: ignore
                    subquery=v_query, name=f"{name}_{count}", iqc=iqc
                )

                sqs.append(sq)
                count += 1

            sq_group = SubQueryGroup(
                subqueries=sqs,
                extension=self,
                subquery=name,  # subqueries are ignored for subquerygroups
                name=f"{name}_group",
                iqc=iqc,
            )

            return [sq_group]
        else:
            return [sq]

    def fix_col_ref(self, opt: str, columns: List[str]):
        if opt in columns:
            return opt
        opt_l = opt.lower().strip()
        opt_ci = next((c for c in columns if c.lower() == opt_l), None)

        if opt_ci is None:
            raise ValueError(f"{opt} not in columns: {columns}")

        return opt_ci

    def apply_pandas_operations_postpivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:
        fillna_opt: str = options.get("fillna")  # type: ignore
        if fillna_opt is not None:
            working_df = working_df.fillna(fillna_opt)

        dropna_opt = options.get("dropna")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def apply_pandas_operations_prepivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:
        # only drops from the "value" column
        fillna_opt: str = options.get("fillna_pre")  # type: ignore
        if fillna_opt is not None:
            logger.debug(f"Filling NaNs with in value column with {fillna_opt}")
            working_df["value"] = working_df["value"].fillna(fillna_opt)

        dropna_opt = options.get("dropna_pre")
        logger.debug(f"Dropping NA from column {dropna_opt}")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def pivot(self, working_df: DataFrame, pivot_option: Union[str, List]) -> DataFrame:
        if pivot_option is None:
            return working_df

        isauto = False
        logger.debug(f"Pivoting by {pivot_option}")
        if isinstance(pivot_option, str):
            if pivot_option.lower() == "none":
                # Pivot disabled / noop
                return working_df
            elif pivot_option.lower() == "auto":
                isauto = True
                index = []
                column = "name"
                value = "value"

                if column not in working_df.columns or value not in working_df.columns:
                    raise ValueError(
                        f"{column} or {value} not found in dataframe columns. Auto should only be used with BQL results."
                    )

                fieldsToCheck = [
                    "id",
                    "orig_ids",
                    "orig_ids:0",
                    "period",
                    "as_of_date",
                    "date",
                ]
                lower_cols = [col.lower() for col in working_df.columns]
                allcols = list(working_df.columns)

                # Case insensitive lookup, but then create an index from the case sensitive names
                for f in fieldsToCheck:
                    if f in lower_cols:
                        index.append(allcols[lower_cols.index(f)])

                if len(index) == 0:
                    index = index[0]
            else:
                raise ValueError("Unexpected pivot setting {pivot_option}")
        elif len(pivot_option) != 2 and len(pivot_option) != 3:
            raise ValueError(f"Unexpected size for pivot options {pivot_option}")
        else:
            index = pivot_option[0]
            column = pivot_option[1]
            value = pivot_option[2] if len(pivot_option) == 3 else "value"

            if index == "auto":
                used_cols = [column.lower(), value.lower()]
                # Use all columns except column and value
                index = [
                    col for col in working_df.columns if col.lower() not in used_cols
                ]
        cols: List[str] = list(working_df.columns)  # type: ignore

        if isinstance(index, list):
            index = [self.fix_col_ref(i, cols) for i in index]
            if len(index) == 1:
                index = index[0]
        else:
            index = self.fix_col_ref(index, cols)

        if isinstance(column, list):
            column = [self.fix_col_ref(i, cols) for i in column]
            if len(column) == 1:
                column = column[0]
        else:
            column = self.fix_col_ref(column, cols)

        if isinstance(value, list):
            value = [self.fix_col_ref(i, cols) for i in value]
            if len(value) == 1:
                value = value[0]
        else:
            value = self.fix_col_ref(value, cols)

        if isinstance(column, list):
            # Needed to allow pivoting by datetime columns
            for col in column:
                if pd.api.types.is_datetime64_any_dtype(working_df[col]):
                    working_df[col] = working_df[col].dt.strftime("%Y-%m-%d")

        logger.debug(f"Pivot index {index} columns {column} values {value}")

        try:
            working_df = working_df.pivot(
                index=index,
                columns=column,
                values=value,
            )
        except Exception as e:
            if not isauto:
                raise e
            else:
                logger.debug("Failed to auto pivot, trying a wider pivot")
                index = [col for col in working_df.columns if col.lower() not in [column.lower(), value.lower()]]  # type: ignore

                working_df = working_df.pivot(
                    index=index,
                    columns=column,
                    values=value,
                )

        working_df = working_df.reset_index()

        if isinstance(value, list) and len(value) > 1:
            working_df.columns = [
                "_".join(reversed(str(col) if type(col) == int else col))
                for col in working_df.columns.values
            ]
        elif isinstance(column, list) and len(column) > 1:
            # Flatten multicolumn indices
            working_df.columns = [
                "_".join(str(col) if type(col) == int else col)
                for col in working_df.columns.values
            ]

        # Clean columns
        renames = {}
        for col in working_df.columns:
            # assert isinstance(col, str)
            colname = col
            newcol = (
                str(colname)
                .replace("#", "")
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "_")
            )
            newcol = newcol.strip("_")
            if col != newcol:
                # columns can't have #, ( or ) symbols
                # logger.debug(f"Replacing {col} with {newcol}")
                renames[col] = newcol

        if len(renames) > 0:
            working_df = working_df.rename(columns=renames)

        return working_df


@dataclass
class SubQuery:
    extension: IqlExtension
    subquery: str
    name: str
    iqc: "IqlQueryContainer"
    dataframe: Optional[DataFrame] = field(default=None, init=False)

    options: Dict[str, object] = field(default_factory=dict, init=False)
    input_data: object = field(default=None, init=False)

    local_dfs: Dict[str, object] = field(default_factory=dict, init=False)

    def get_subqueries_flat(self) -> List["SubQuery"]:
        return [self]

    def merge(self):
        # Nothing to do for a single subquery
        pass

    def get_query(self) -> str:
        """Returns the first parameter to:
        keyword(query, *params)"""
        if len(self.options) == 0:
            raise ValueError(f"Options not properly passed or parsed ({self.subquery})")

        query = next(iter(self.options.keys()))
        return query

    def __post_init__(self):
        if self.subquery is not None:
            self.options: Dict[str, object] = options_parser.options_to_list(
                self.subquery
            )
            logger.debug(f"Options: {self.options}")

    def populate_from_cache(self) -> bool:
        """Returns cached value if it's available"""
        cache_val = self.subquery

        logger.debug(f"Checking cache for {cache_val}, {type(self)}")
        if not self.extension.allow_cache_read(self):
            return False

        df = qc.get(key=cache_val, use_file_cache=self.extension.use_file_cache())
        if df is not None:
            logger.debug("Using cached SubQuery")
            self.dataframe = df  # type: ignore
            return True
        else:
            logger.debug("Not found in cache")
            return False

    def save_to_cache(self):
        if not self.extension.allow_cache_save(self):
            return

        cache_period = self.extension.get_cache_period()

        cache_override = self.options.get("cache")
        if cache_override is not None:
            if isinstance(cache_override, int):
                cache_period = cache_override
            else:
                raise ValueError(f"Invalid cache value passed: {cache_override}")

        cache_val = self.subquery

        logger.debug(
            f"Saving to cache {cache_val} {self.extension.get_cache_period()} override {cache_override}"
        )

        if self.dataframe is not None:
            qc.save(
                key=cache_val,
                o=self.dataframe,
                duration_seconds=cache_period,
                use_file_cache=self.extension.use_file_cache(),
            )


@dataclass
class SubQueryGroup(SubQuery):
    """SubQueryGroups represent a set of queries whose outputs will be combined.
    SubQueries are executed in parallel (via get_subqueries_flat),
    so this step is needed to gather the results.

    Our first implementation was to rely on database Unions, but performance wasn't
    great.

    Future: SubQueryGroups could support nesting, only one level supported now."""

    subqueries: List[SubQuery]

    def __post_init__(self):
        self.subquery = None  # type: ignore
        self.options = None  # type: ignore

    def get_subqueries_flat(self) -> List[SubQuery]:
        return self.subqueries

    def get_query(self) -> str:
        raise ValueError("SubQueryGroups do not have a query")

    def merge(self):
        """Since each file may have a different schema, we'll read them all and let's Pandas concat
        sort it out. Using DuckDb "union by name" ran into an error (hash table memory)
        """

        if self.extension.use_path_replacement():
            files = [
                self.extension.get_path_replacement(sq, quote=False)
                for sq in self.subqueries
            ]

            logger.info(f"Read {len(files)} parquet files")

            dfs = [pd.read_parquet(f) for f in files]
            logger.info("Done reading, concatting")

            df = pd.concat(dfs)

            outfile = self.extension.get_path_replacement(self, quote=False)
            logger.info(f"Writing to final parquet file {outfile}")

            df.to_parquet(outfile)

        else:
            dfs: List[DataFrame] = [sq.dataframe for sq in self.subqueries]  # type: ignore
            logger.debug(f"Concatting {len(dfs)}")
            self.dataframe = pd.concat(dfs)

        logger.info(f"Done merging {len(self.subqueries)} subqueries")


class IqlQueryContainer:
    # This is used so we can run the bql_queries as an async batch, separate from processing the results.
    orig_query: str
    query: str
    subqueries: List[SubQuery]
    db: Optional[object]

    def extract_subqueries(self):
        subqueries: List[SubQuery] = []

        i = 0

        replacements: Dict[str, Optional[str]] = {}

        if "--" in self.orig_query:
            query = sqlparse.format(self.orig_query, strip_comments=True).strip()
        else:
            query = self.orig_query

        for keyword, subword, outer, inner in _extract_subquery_strings(query):
            i += 1
            name = f"{_DFPREFIX}_{i}"

            extension = get_extension(keyword, subword)
            sqs: List[SubQuery] = extension.create_subqueries(
                query=outer, name=name, iqc=self
            )
            subqueries.extend(sqs)

            if extension.use_path_replacement():
                names = [sq.extension.get_path_replacement(sq) for sq in sqs]
            else:
                names = [sq.name for sq in sqs]

            if len(names) == 1:
                result = names[0]
            else:
                querystrings = [f"(select * from {i})" for i in names]

                result = " UNION ".join(querystrings)
                result = f"({result})"

            replacements[outer] = result

        for old, new in replacements.items():
            logger.debug(f"Replacing {old} with {new}")
            query = query.replace(old, new)  # type: ignore

        # if only one function without a beginning subquery
        if len(replacements) > 0:
            values = [value for value in replacements.values() if value is not None]
            if re.match(rf"(?s)\s*({'|'.join(values)}).*", query) is not None:
                logger.info(f"Starts with replacement {values}")
                query = f"select * from {query}"

        self.query = query

        return subqueries

    def __init__(self, query: str, db: IqlDatabase):
        self.orig_query = query
        self.query = query
        self.db = db

        self.subqueries = self.extract_subqueries()
        # self.subqueries = self._extract_replacements()
        # Sanity checks. These don't take into account escaping or quoting, so they're just warnings.
        if query.count("(") != query.count(")"):
            logger.warning("Left and Right Paren counts aren't equal")

        if query.count("'") % 2 != 0:
            logger.warning("Uneven number of single quotes")

        if query.count('"') % 2 != 0:
            logger.warning("Uneven number of double quotes")

    def get_subqueries_by_extension(self, keyword: str, subword: str) -> List[SubQuery]:
        results: List[SubQuery] = []
        results = [
            s
            for s in self.subqueries
            if s.extension.keyword == keyword and s.extension.subword == subword
        ]

        return results

    def execute(self) -> Tuple[Optional[DataFrame], List[DataFrame]]:
        """Returns the final df, plus the intermediate subquery dataframes.
        If the query is not a Select, returns a None"""
        # Execute the subqueries

        completed_dfs: Dict[str, DataFrame] = {}

        for (keyword, subword), e in _EXTENSIONS.items():
            sqs: List[SubQuery] = self.get_subqueries_by_extension(keyword, subword)  # type: ignore

            e_dfs = e.execute_batch(sqs)  # type: ignore

            for k, df in e_dfs.items():
                if df is not None:
                    completed_dfs[k] = df

        result = self.db.execute_query(query=self.query, completed_dfs=completed_dfs)  # type: ignore
        df = result.df_numpy()

        return (df, completed_dfs)  # type: ignore


class IqlPlan:
    pass


def _parameterize_sql_alias(subword, query) -> str:
    if subword not in _ALIASES.keys():
        raise ValueError(f"Unknown alias {subword}")

    base_query = _ALIASES[subword]

    for k, v in options_parser.options_to_list(query).items():
        # convert the parameter to $uppercase, so security => $SECURITY
        newk = f"${k.upper()}"
        if newk not in base_query:
            raise ValueError(f"Parameter {k} / {newk} not in alias SQL")
        else:
            base_query = base_query.replace(newk, str(v))

    return base_query


def replace_sql_aliases(query) -> str:
    newquery = query
    for keyword, subword, outer, inner in _extract_subquery_strings(query, ["alias"]):
        sql = _parameterize_sql_alias(subword, outer)

        logger.debug(f"Found SQL alias, replacing and parameterizing: {outer}")

        newquery = newquery.replace(outer, sql)
        # logger.info(f"After alias replacement {query}")

    return newquery


def execute_full_results(
    query: str, con: Optional[object] = None
) -> Tuple[Optional[DataFrame], Optional[List[DataFrame]], IqlPlan]:
    # Connection to database
    get_dbconnector()
    if _DBCONNECTOR is None:
        raise ValueError("DBConnector Not Set")
    if con is None:
        db = _DBCONNECTOR.create_database()
    else:
        db = _DBCONNECTOR.create_database_from_con(con=con)

    # Aliases
    query = replace_sql_aliases(query)

    # Placeholder for an IqlPlan (noop for now)
    iqlplan: IqlPlan = IqlPlan()

    try:
        # A single query might contain multiple SQL statements. Parse them out and iterate:

        df = None
        completed_dfs = None
        if ";" not in query:
            # Performance optimization for simple queries
            iqc = IqlQueryContainer(query=query, db=db)

            df, completed_dfs = iqc.execute()
        else:
            for statement in sqlparse.parse(query):
                singlequery = statement.value.strip(";")
                iqc = IqlQueryContainer(query=singlequery, db=db)

                # Run each statement, but only keep the results from the last one
                df, completed_dfs = iqc.execute()

        # The first result is the query result. The other df's are for debugging purposes
        # If it's not a select, there won't be response, such as in a COPY (..) TO

        return (df, completed_dfs, iqlplan)

    finally:
        if con is None:  # DB was created here, so close it
            db.close_db()


def execute(query: str, con: Optional[object] = None) -> Optional[DataFrame]:
    """Executes the given SQL query. Keyword is only used to run a single subquery without SQL."""

    if query.strip().startswith("get") or query.strip().startswith("let"):
        query = query.replace('"', '"')
        query = f"""select * from bql("{query}")"""
    df, completed_dfs, iql_plan = execute_full_results(query, con)

    return df


def get_dbconnector() -> IqlDatabaseConnector:
    global _DBCONNECTOR
    if _DBCONNECTOR is None:
        # Initializes only on first reference
        module = importlib.import_module(DB_MODULE)
        _DBCONNECTOR = module.getConnector()

    if _DBCONNECTOR is None:
        raise ValueError("Failure initializing _DBCONNECTOR")
    return _DBCONNECTOR


def register_extension(e: IqlExtension):
    _EXTENSIONS[(e.keyword, e.subword)] = e  # type: ignore
    if e.keyword not in _KNOWN_EXTENSIONS.keys():
        _KNOWN_EXTENSIONS[e.keyword] = e.keyword

    if e.temp_file_directory is None:
        e.temp_file_directory = DEFAULT_EXT_DIRECTORY


def register_alias(subword: str, sql: str):
    """
    Aliases are called via
    alias.aliasname(param1=abc, param2.abc)
    When run, the alias will be replaced, and "$PARAM1" will be replaced with abc
    """
    logger.debug(f"Registering alias: {subword}")
    _ALIASES[subword] = sql


def list_extensions() -> List[str]:
    return list(_KNOWN_EXTENSIONS.keys())


def get_extension(keyword: str, subword: str) -> "IqlExtension":
    """Loads extension on first use"""

    words = (keyword, subword)
    if words in _EXTENSIONS:
        return _EXTENSIONS[words]
    elif keyword not in _KNOWN_EXTENSIONS.keys():
        raise ValueError(f"Unknown Extension {keyword}")
    else:
        # Dynamically load extensions on first use
        # This avoids requiring installation of packages that
        # aren't needed
        classname = _KNOWN_EXTENSIONS[keyword]
        module = importlib.import_module(classname)
        module.register(keyword)

        if words not in _EXTENSIONS:
            raise ValueError(f"{keyword}.{subword} is not registered")
        return _EXTENSIONS[words]


def configure(
    duration_seconds: Optional[int] = -1,
    cache_directory: Optional[str] = None,
    temp_dir: Optional[str] = None,
    max_processes: Optional[int] = None,
):
    """
    Must be called before extensions are initialized (on first use)
    duration_seconds: None (Disabled), -1 (Infinite), int (Seconds)
    file_directory: None (no file cache), string (output directory)
    """
    global _CACHE_PERIOD
    global _USE_FILE_CACHE
    global DEFAULT_EXT_DIRECTORY

    _CACHE_PERIOD = duration_seconds
    if cache_directory is None:
        _USE_FILE_CACHE = False
    else:
        _USE_FILE_CACHE = True
        if not os.path.exists(cache_directory):
            raise ValueError(f"cache_directory {cache_directory} does not exist")

        qc.activate_file_cache(cache_directory)

    DEFAULT_EXT_DIRECTORY = temp_dir

    if max_processes is not None:
        te.MAX_PROCESSES = max_processes

# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import duckdb
import logging
from contextlib import nullcontext
from typing import Dict, Optional

from pandas import DataFrame
from pandas import ArrowDtype
from pyarrow import Table

from iql.iqmoql import IqlDatabaseConnector, IqlDatabase, IqlResult
import threading

from dataclasses import dataclass

logger = logging.getLogger(__name__)


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
class DuckDbResult(IqlResult):
    _table: Table

    def arrow(self):
        return self._table

    def df_numpy(self):
        return self._table.to_pandas()

    def df_arrow(self):
        return self._table.to_pandas(types_mapper=ArrowDtype)


@dataclass
class _DuckDB(IqlDatabase):
    _connection: object
    _started_thread: int

    def execute_query(
        self, query: str, completed_dfs: Optional[Dict[str, DataFrame]] = None
    ) -> Optional[DuckDbResult]:
        """param: Each of the completed _dfs are registered to the database.
        threaded: pass True to run in a separate connection, otherwise runs in main connection
        """

        threaded = threading.get_ident() != self._started_thread

        # create & close the connection if we're threading, otherwise create one
        with self.get_connection() if threaded else nullcontext(
            self._connection
        ) as con:
            try:
                # Register each of the dataframes to duckdb, so duckdb can query them
                # Other database might require a "load" or "from_pandas()" step to load these
                # to temporary tables.
                if completed_dfs is not None:
                    for key, df in completed_dfs.items():
                        if df is None or (df.empty and len(df.columns) == 0):
                            continue
                            # raise ValueError(f"None dataframe for {key}")
                        con.register(key, df)  # type: ignore

                d = con.execute(query)  # type: ignore
                # Don't use con.sql, as it adds a small but
                # measurable overhead of creating a duckdb relation, that we don't need
                if d is not None:
                    # logger.debug("Using Pandas format")
                    try:
                        table = d.arrow()
                        return DuckDbResult(_table=table)
                    except Exception:
                        # TODO: Detect this more gracefully
                        logger.debug("Didn't have a result set {str(e)}")
                        return None

                else:
                    return None
            except Exception as e:
                logger.exception(f"Error executing SQL DFs: {query}")
                raise e

    def get_connection(self):
        return self._connection.cursor()  # type: ignore

    def close_db(self):
        try:
            if self._connection is None:
                return
            else:
                self._connection.close()  # type: ignore
                self._connection = None
        except Exception:
            logger.exception("Unable to close")


class _DuckDbConnector(IqlDatabaseConnector):
    def create_database(self) -> _DuckDB:
        con = duckdb.connect(database=":memory:")
        return _DuckDB(_connection=con, _started_thread=threading.get_ident())

    def create_database_from_con(self, con: object) -> _DuckDB:
        return _DuckDB(_connection=con, _started_thread=threading.get_ident())


def getConnector() -> IqlDatabaseConnector:
    return _DuckDbConnector()

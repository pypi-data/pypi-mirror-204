# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqlExtension, register_extension, SubQuery, IqlDatabase
import pyarrow as pa
import pandas as pd

logger = logging.getLogger(__name__)


def get_data(sq: SubQuery, source_query) -> pd.DataFrame:
    db: IqlDatabase = sq.iqc.db  # type: ignore
    input_data = sq.input_data
    local_dfs = sq.local_dfs

    # So much work to get Polars and/or PyArrow to work in sklearn
    # Can revisit, but need to work around using onehotencoder
    if input_data is not None:
        if isinstance(input_data, DataFrame):
            return input_data
        elif isinstance(input_data, pa.lib.Table):
            return input_data.to_pandas()  # type: ignore
        else:
            raise ValueError(f"Unexpected type: {type(input_data)}")

    else:
        result = db.execute_query(  # type: ignore
            query=source_query, completed_dfs=local_dfs
        )
        if result is None:
            raise ValueError(f"Could not get data for query {source_query}")
        else:
            return result.df_numpy()


def get_query_from_options(options) -> str:
    sql = options.get("sql")
    if sql is not None:
        return sql

    dfname = options.get("df")
    tablename = options.get("table")

    if dfname is not None:
        return f"select * from {dfname}"
    elif tablename is not None:
        return f"select * from {tablename}"

    dataname = options.get("data")
    if dataname is not None:
        if " " in dataname:
            return dataname
        else:
            return f"select * from {dataname}"

    raise ValueError("df, table, sql and data are not specified")


@dataclass
class PandasExtension(IqlExtension):
    keyword: str

    def allow_cache_read(self, sq: SubQuery) -> bool:
        # Never cache, because this depends on contents of table
        return False

    def allow_cache_save(self, sq: SubQuery) -> bool:
        return False

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        query = get_query_from_options(sq.options)

        return get_data(sq, query)


def register(keyword: str):
    extension = PandasExtension(keyword=keyword)
    register_extension(extension)

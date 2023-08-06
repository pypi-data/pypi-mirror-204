# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved
#

from typing import List
import concurrent.futures as cf
import logging
from iql import iqmoql

import inspect

logger = logging.getLogger(__name__)

ENABLED = True
MAX_PROCESSES = 4


def _get_name_from_framestack(name: str) -> object:
    """When we're threading, the database layer can't inspect the call stack."""
    frame = inspect.currentframe()

    while frame is not None and hasattr(frame, "f_locals"):
        if frame is None:
            return None
        o = frame.f_locals.get(name)  # type: ignore
        if o is not None:
            return o
        else:
            frame = frame.f_back  # type: ignore

    return None


def load_local_dfs(sq: "iqmoql.SubQuery"):
    """This is needed because the thread call stacks are different, thus won't find any local variables.
    This is comparable to what DuckDB does to discover dataframes."""
    df_possible_names = ["data", "df", "sql", "data1", "data2"]

    for name in df_possible_names:
        opt: str = sq.options.get(name)  # type: ignore
        if opt is None:
            continue
        else:
            o = _get_name_from_framestack(opt)

            if o is None:
                logger.info(f"Couldn't load {opt} from currentframes")
            if o is not None:
                logger.debug(f"Registering {opt}")
                sq.local_dfs[opt] = o


def execute_batch(subqueries_flat: List["iqmoql.SubQuery"], execute):
    processPool = cf.ThreadPoolExecutor(MAX_PROCESSES)

    futures = []
    futuretuples = []
    for query in subqueries_flat:
        # when running parallel, subqueries can't use the DuckDB connections

        # for threads to run parallel, use separate cursors:
        # https://duckdb.org/docs/guides/python/multiple_threads

        load_local_dfs(query)
        logger.debug("Submitting")
        f = processPool.submit(execute, query)

        futures.append(f)
        futuretuples.append((f, query))

    logger.debug("Waiting")

    cf.wait(futures)
    logger.debug("Done Waiting")

    for f, sq in futuretuples:
        sq.dataframe = f.result()

    logger.debug("Done reading")

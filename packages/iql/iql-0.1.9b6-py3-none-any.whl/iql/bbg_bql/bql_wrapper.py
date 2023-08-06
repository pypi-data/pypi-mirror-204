# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

""" This module wraps the Bloomberg BQL API to provide
consistent return results """

import time
import logging
from threading import Lock
from datetime import datetime
from functools import partial
from typing import List, Optional, Union, Dict
from pandas import DataFrame
from abc import abstractmethod

import bql  # pyright: ignore pylint: disable=C0413 # noqa: E402
from iql import q_cache
from iql import iqmoql


_MAX_CONCURRENT = 128
_SHIFT_DUPLICATES = True

logger = logging.getLogger(__name__)

bqService = None
_disabled = False

# Used to avoid multiple threads from simultaneously running bql statements
bqllock = Lock()


class BaseBqlQuery:
    STATUS_NOTRUN = "NOTRUN"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_FAILURE = "FAILURE"

    execution_status: str = STATUS_NOTRUN
    exception_msg: Optional[str] = None
    _data: Optional[List[Dict[str, object]]] = None
    _df: Optional[DataFrame] = None

    params = None

    @abstractmethod
    def get_fields(self) -> List[str]:
        pass

    @abstractmethod
    def to_bql_query(self) -> str:
        pass

    def execute(self) -> bool:
        """Executes the query and, if successful, sets the query._data"""
        try:
            self._populate_data()
            return self.execution_status == self.STATUS_COMPLETED
        except Exception as e:
            logger.exception("execute")
            self.execution_status = self.STATUS_FAILURE
            self.exception_msg = str(e)
            return False

    def to_data(self) -> List[Dict[str, object]]:
        """Internal representation"""
        if self._data is not None:
            return self._data
        else:
            success = self.execute()
            if not success or self._data is None:
                raise ValueError("Failure executing BQL query")
            else:
                return self._data

    def to_df(self) -> DataFrame:
        if self._df is None:
            self._df = DataFrame(self._data)
        return self._df

    def _populate_data(self):
        execute_bql_str_list_async_q([self])


def get_bqservice(retries: int = 3):
    global bqService
    logger.debug("Creating new bqService")

    try:
        if bqService is None:  # type: ignore
            bqService = bql.Service()  # (bqlmetadata.ShippedMetadataReader())
    except Exception as e:
        logger.exception("Unable to create bq service")
        if retries <= 0:
            raise e

    if bqService is None:
        if retries > 0:
            logger.warning(f"Retry get bqservice (retries left {retries})")
            return get_bqservice(retries - 1)
        raise ValueError("Unable to obtain bql.Service()")
    return bqService


def close_bqservice():
    """Closing the session is not normally needed, but there is a limit on the number of concurrent connections.
    BQL uses (as far as we can tell) a Singleton so multiple bql sessions requests will not consume more connections.
    """
    try:
        global bqService
        if bqService is None or bqService._Service__bqapi_session is None:  # type: ignore
            logger.info("_Service__bqapi_session already closed or None")
            return
        else:
            logger.info("Closing _Service__bqapi_session session")
            bqService._Service__bqapi_session.close()  # type: ignore
            bqService = None
    except Exception:
        logger.exception("Error closing bqapi session")


def list_to_str(values: list, quote: bool = False, delimiter: str = ", \n") -> str:
    """Helper to convert list of values to a comma delimited list. Used for BQL functions.
    Equity lists should be quoted"""

    if quote:
        return delimiter.join(f"'{val}'" for val in values)
    else:
        return delimiter.join(values)


def clean_field_name(fieldname):
    """Strips whitespace and &s from parameter names.
    Used for converting BDP fields to BQL fields"""
    return (
        fieldname.replace(" ", "_")
        .replace("_&_", "_AND_")
        .replace("&", "_AND_")
        .upper()
    )


def security_to_finalstr(security: Union[str, List]) -> str:
    # if isinstance(security, List):
    #    field_str = list_to_str(security, False)

    if isinstance(security, str) and (
        "(" in security or "[" in security or "$" in security
    ):
        final_security_str = security
    elif isinstance(security, str):
        if "'" not in security:
            security = "'" + security + "'"
        final_security_str = "[" + security + "]"
    else:  # isinstance(security, List):
        final_security_str = list_to_str(security, True)
        final_security_str = "[" + final_security_str + "]"

    return final_security_str


def construct_bql_query(
    field_str: Union[str, List],
    security: Union[List[str], str],
    with_params: Optional[str] = None,
    let_vars: Optional[str] = None,
) -> str:
    """Simple wrapper to construct a valid BQL query string from an
    already comma delimited list of fields and quoted securities"""

    # Better to use BQLQuery, but leaving this for now.

    if isinstance(field_str, List):
        field_str = list_to_str(field_str, False)

    final_security_str = security_to_finalstr(security)

    request_str = ""
    if let_vars is not None:
        request_str += "let (" + let_vars + ")"

    request_str += "get("
    request_str += field_str

    request_str += ") for (" + final_security_str + ")"

    # default WITH clause
    # TODO: Replace this with something metadata driven, since it may not be applicable in all cases
    # request_str += "\nwith (fill=prev)"

    if with_params is not None:
        request_str += " with (" + with_params + ")"

    if "preferences" not in request_str:
        request_str += "\npreferences (addcols=all)"

    return request_str


def error_callback(o):
    # TODO: Pass with some context information using a partial()
    logger.warning("Error executing" + str(o))


def execute_bql_str_list_async_q(
    queries_input: List[BaseBqlQuery],
    suppress_warning_log: bool = False,
    max_queries: int = _MAX_CONCURRENT,
):
    if _disabled:
        raise ValueError("BQL is disabled")
    """Note: Not multi-process safe due to underlying BQL APIs
    and (presumably) its use a Singleton for bqapi requests.
    Either batch requests through a single requester thread, or
    distribute workload across requesters.
    """
    logger.debug("Checking to see if any are already cached")

    for q in queries_input:
        qstr = q.to_bql_query()
        data = q_cache.get(qstr)  # type: ignore
        if data is not None:
            logger.debug(f"Found in cache: {qstr}")

            if isinstance(data, DataFrame):
                q._df = data
            else:
                q._data = data  # type: ignore
            q.execution_status = q.STATUS_COMPLETED

    queries_not_cached = [q for q in queries_input if q._data is None]

    """Max Queries indicates the max per batch: chop the queries
    into smaller groups of max_queries size and execute each serially"""

    if len(queries_not_cached) == 0:
        logger.debug("No queries to run")
        return

    query_groups = [
        queries_input[i * max_queries : (i + 1) * max_queries]
        for i in range((len(queries_not_cached) + max_queries - 1) // max_queries)
    ]

    start = time.time()

    count = 1
    for query_group in query_groups:
        logger.info(
            f"Executing {count} of {len(query_groups)} query batches with {len(query_group)} queries"
        )
        count = count + 1

        # t1 = threading.Thread(target=asyncio.run, args=(_execute_bql_str_list_async_callbacks(query_group, suppress_warning_log),))
        # t1.start()
        # t1.join

        logger.debug("Done async with callbacks")
        _execute_bql_str_list_async_orig(query_group, suppress_warning_log)

    end = time.time()
    logger.info(f"Elapsed time running queries: {end-start} seconds")

    for q in queries_not_cached:
        logger.debug("Saving to cache")
        if q._data is not None:
            q_cache.save(
                q.to_bql_query(),
                q._data,
                type=__name__,
                duration_seconds=iqmoql._CACHE_PERIOD,
            )

    return


def submit_fetch_many_available():
    # Force execute_many for now.
    # return os.environ.get("BQUANT_USERNAME") is not None

    return False


def _execute_bql_str_list_async_orig(
    queries: List[BaseBqlQuery], suppress_warning_log: bool = False
):
    with bqllock:
        query_strings = []
        for query in queries:
            qstr = query.to_bql_query()

            if "iqmo" in qstr:
                raise ValueError("IQMO parameters passed to BQL layer, cannot run")

            logger.debug(f"Executing {qstr}")
            query_strings.append(qstr)

        bqService = get_bqservice()
        # error_list: List[str] = []

        if submit_fetch_many_available():
            logger.debug("Using submit fetch many")
            gen = bqService.submit_fetch_many(
                query_strings, on_request_error=error_callback
            )
        else:
            gen = bqService.execute_many(
                query_strings,
                partial(error_callback),
            )

        error_index = 0

        logger.info("Waiting for and processing BQL results")
        for r, q in zip(gen, queries):
            try:
                if r is None:
                    q.execution_status = q.STATUS_FAILURE
                    logger.warn(f"Error executing: {q.to_bql_query()}")
                    q.exception_msg = "Failure"
                    error_index = error_index + 1
                else:
                    data = _to_data(r)
                    q._data = data
                    q.execution_status = q.STATUS_COMPLETED

            except Exception as e:
                logger.exception("Query error")
                q._data = None
                q.execution_status = q.STATUS_FAILURE
                q.exception_msg = str(e)
        logger.info("Done executing")


def flatten_list_str(value: Union[str, List[str]]) -> List[str]:
    """Converts input to a List, if not already a List"""
    if isinstance(value, str):
        value_str = str(value)

        value_list = [value_str]
        return value_list
    else:
        return value


def _process_single_item_response(
    res: bql.SingleItemResponse,
    result_table,
    shift_duplicates: bool = _SHIFT_DUPLICATES,
    replaceNanInfsWithNone: bool = True,
):
    name = res.name
    logger.debug(f"Processing {name}")

    values = res._SingleItemResponse__result_dict.get("valuesColumn").get("values")  # type: ignore
    values_type = res._SingleItemResponse__result_dict.get("valuesColumn").get("type")  # type: ignore

    secondary_cols = res._SingleItemResponse__result_dict.get("secondaryColumns")  # type: ignore
    # dates = [col for col in secondary_cols if col.get("name") == "DATE"]

    id_col = res._SingleItemResponse__result_dict.get("idColumn")  # type: ignore
    if id_col is not None:
        id_values = id_col.get("values")
    else:
        id_values = None

    for i in range(0, len(values)):
        row = dict()
        row["name"] = name

        if (
            values_type is not None
            and values_type == "DATE"
            and values[i] is not None
            and len(values[i]) > 0
        ):
            date_val = datetime.strptime(values[i], "%Y-%m-%dT%H:%M:%S%z")
            date_val = date_val.replace(tzinfo=None)
            row["value"] = date_val

        elif (
            replaceNanInfsWithNone
            and values_type == "DOUBLE"
            and values[i] in ["NaN", "Infinity", "-Infinity"]
        ):
            row["value"] = None
        else:
            row["value"] = values[i]

        if id_values is not None and len(id_values) > 0:
            row["id"] = id_values[i]

        for col in secondary_cols:
            col_name = col.get("name")
            col_values = col.get("values")

            if shift_duplicates:
                # append unique identifier to duplicate columns
                if col_name in row.keys():
                    c: int = 1
                    tempcolname = col_name
                    while tempcolname in row:
                        tempcolname = f"{col_name}_{c}"
                        c += 1
                    col_name = tempcolname

            if len(col_values) > 0:
                if col_name == "DATE" or (
                    "type" in col.keys() and col["type"] == "DATE"
                ):
                    date_str = col_values[i]
                    if date_str is not None:
                        date_val = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
                        date_val = date_val.replace(tzinfo=None)
                        row[col_name] = date_val
                else:
                    row[col_name] = col_values[i]

        result_table.append(row)


def _process_response(response: bql.Response, result_table):
    if response is None:
        return
    for res in response:
        if isinstance(res, bql.SingleItemResponse):
            _process_single_item_response(res, result_table)
        else:
            # Sometimes, there are multiple levels to the responses
            _process_response(res, result_table)


def _to_data(response: bql.Response) -> List[Dict[str, object]]:
    """Converts BQL Response to a List of Dicts, where each dict contains Col: Value"""
    result_table: List = []

    _process_response(response, result_table)

    return result_table

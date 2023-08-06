# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import requests
import logging
from dataclasses import dataclass
from typing import List, Dict
from pandas import DataFrame
from iql.iqmoql import IqlExtension, register_extension, SubQuery

logger = logging.getLogger(__name__)
FRED_API_KEY = None

_FRED_TYPES = [
    {
        "name": "releases",
        "reqoptions": {},
        "url": "https://api.stlouisfed.org/fred/releases",
    },
    {
        "name": "series",
        "reqoptions": {"seriesid": "SERIESID"},
        "url": "https://api.stlouisfed.org/fred/series?series_id=SERIESID",
    },
    {
        "name": "observations",
        "reqoptions": {"seriesid": "SERIESID", "startdate": "STARTDATE"},
        "url": "https://api.stlouisfed.org/fred/series/observations?series_id=SERIESID&observation_start=STARTDATE",
    },
]


def options_to_url(
    type_name: str, sq: SubQuery, options_def: List[Dict], constants_to_add: Dict
) -> str:
    name, reqoptions, url = next(
        (
            (v["name"], v["reqoptions"], v["url"])
            for v in options_def
            if v["name"] == type_name
        ),
        (None, None, None),
    )

    if name is None:
        raise ValueError(f"Unknown type: {type_name}")
    else:
        query_string: str = url  # type: ignore

    for ro_k, ro_v in reqoptions.items():  # type: ignore
        if ro_k not in sq.options:
            raise ValueError(f"{type_name} requires {ro_k} to be set")
        else:
            query_string = query_string.replace(ro_v, sq.options.get(ro_k))  # type: ignore
            constants_to_add[ro_k] = sq.options.get(ro_k)  # type: ignore

    return query_string


def get_url(sq: SubQuery, constants_to_add: Dict, types: List[Dict]) -> str:
    first_option_k, first_option_v = next(
        ((k, v) for k, v in sq.options.items()), (None, None)
    )
    if first_option_v is None:
        fred_url = first_option_k  # type: ignore
    else:
        fred_url = sq.options.get("url")  # type: ignore

    fred_type: str = sq.options.get("type")  # type: ignore

    if fred_type is None and fred_url is None:
        raise ValueError("Either type='' or url='' must be passed for FRED")

    if fred_type is not None:
        query_string = options_to_url(
            type_name=fred_type,
            sq=sq,
            options_def=types,
            constants_to_add=constants_to_add,
        )

    else:
        query_string: str = fred_url  # type: ignore

    return query_string


@dataclass
class FredExtension(IqlExtension):
    keyword: str

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        constants_to_add = {}

        query_string = get_url(sq, constants_to_add, _FRED_TYPES)
        if FRED_API_KEY is None:
            raise ValueError("FRED_API_KEY not set, cannot run")
        else:
            if "api_key" in query_string:
                raise ValueError("api_key is hardcoded in the query")
            elif "file_type" in query_string and "file_type=json" not in query_string:
                raise ValueError("file_type is set, and not to JSON")
            else:
                if "?" not in query_string:
                    query_string += "?"
                query_string += f"&api_key={FRED_API_KEY}"
                if "file_type=json" not in query_string:
                    query_string += "&file_type=json"

                logger.info(f"Querying: {query_string}")
                resp = requests.get(query_string)
                if resp.status_code != 200:
                    raise ValueError(
                        f"Received status {resp.status_code}, cannot process. Result: {resp.text}"
                    )

                json = resp.json()

                firstlist = next(
                    (value for value in json.values() if isinstance(value, list)), None
                )

                if firstlist is None:
                    dataframe = DataFrame(json)
                else:
                    dataframe = DataFrame(firstlist)

                for k, v in constants_to_add.items():
                    dataframe[k] = v
                return dataframe


def register(keyword: str):
    extension = FredExtension(keyword=keyword)
    register_extension(extension)

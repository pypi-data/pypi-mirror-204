# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import requests
import logging
import numpy
import re
import os
from typing import Dict, List, Optional
from pandas import DataFrame  # read_fwf
from iql.iqmoql import IqlExtension, register_extension, SubQuery
from iql.extensions import fred_extension as fe

# import base64
# from io import BytesIO
# import pathlib

logger = logging.getLogger(__name__)


EDGAR_USER_AGENT = None

# Note the {}'s aren't used in actual f-strings
# These are string-replaced
_EDGAR_TYPES = [
    {
        "name": "ciks",
        "reqoptions": {},
        "url": "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt",
    },
    {
        "name": "submissions",
        "reqoptions": {"cik": "{CIK}"},
        "url": "https://data.sec.gov/submissions/CIK{CIK}.json",
    },
    {
        "name": "facts",
        "reqoptions": {"cik": "{CIK}"},
        "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json",
    },
    {
        "name": "concepts",
        "reqoptions": {"cik": "{CIK}", "ftype": "{ftype}", "field": "{field}"},
        "url": "https://data.sec.gov/api/xbrl/companyconcept/CIK{CIK}/{ftype}/{field}.json",
    },
    {
        "name": "frame",
        "reqoptions": {"frame": "{frame}", "field": "{field}"},
        "url": "https://data.sec.gov/api/xbrl/frames/us-gaap/{field}/USD/{frame}.json",
    },
]


def flatten_to_first_list(d, stack: List[Dict], rows: List[Dict]):
    """Recursively builds a List[Dict] from JSON, building a stack of parent key/values.
    When it encounters a list, it creates a Dict for each list element combined with the stacks key/values.
    If the list contains anything other than a Dict, raises an Exception"""

    if type(d) is dict:
        vals = {}
        for k, v in d.items():
            # First, capture the scalar values at this level and push onto the stack
            if type(v) is not dict and type(v) is not list:
                # Scalar
                vals[k] = v
        stack.append(vals)

        # Next, process any dict items:

        for k, v in d.items():
            # Store the dict key as the name for the level
            if type(v) is dict:
                vals[f"level_{len(stack)}"] = k
                flatten_to_first_list(v, stack, rows)
            if type(v) is list:
                # Assumes each element in the list is a dict
                for i in v:
                    rowvals = {}
                    for s in stack:
                        rowvals.update(s)

                    rowvals["list"] = k
                    if numpy.isscalar(i):
                        rowvals["val"] = i
                    elif type(i) is not dict:
                        raise ValueError(f"Unexpected list element type: {type(i)}")
                    else:
                        rowvals.update(i)

                    rows.append(rowvals)
    stack.pop()


def to_df(json) -> DataFrame:
    """Converts an Edgar JSON response to a DataFrame"""
    stack = []
    rows = []

    flatten_to_first_list(json, stack, rows)
    return DataFrame(rows)


def _request_edgar(url: str) -> object:
    if EDGAR_USER_AGENT is None:
        raise ValueError(
            """Set iql.extension.edgar_extension.user_agent to: 'Your Company 'your@email.address') . 
            See https://www.sec.gov/os/webmaster-faq#developers for more info."""
        )

    global prefix

    # Add headers
    logger.debug(f"Requesting {url}")
    headers = {"User-Agent": EDGAR_USER_AGENT}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        # display(response.content.decode())
        raise ValueError(f"Error: {response.status_code}: {response.content.decode()}")
    else:
        # display(response.encoding)
        return response


def edgar_request_to_df(url: str) -> DataFrame:
    rawdata = _request_edgar(url)
    data = rawdata.json()  # type: ignore

    if "filings" in data:
        if "recent" in data["filings"]:
            d = data["filings"]["recent"]

            return DataFrame.from_dict(d, orient="index").transpose()

    df = to_df(data)
    return df


# lastresponse = None

lookup_re = re.compile(r"\s*(.*)\:(.*?)\:\s*")


class EdgarExtension(IqlExtension):
    """Keyword: the function name used in the SQL, such as query_somesite(...)
    base_url: The constant part of the URL path, such as https://www.somesite.com/abc/api
    path: The variable part of the URL path, which will be passed in the function as: query_somesite(path='/data/something',

    """

    keyword: str
    base_url: str
    path: Optional[str]

    constant_params: Dict[str, str]

    # Params that will always be passed, such as:
    # api_key: somekey
    # or file_type: json

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        constants_to_add = {}

        url = fe.get_url(sq, constants_to_add, _EDGAR_TYPES)

        # for https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"
        if url.endswith(".txt"):
            res = _request_edgar(url)
            # data_str = StringIO(res.text)

            tempfilename = url[url.rindex("/") + 1 :]

            if self.temp_file_directory is None:
                tempfilepath = tempfilename
            else:
                tempfilepath = os.path.join(self.temp_file_directory, tempfilename)

            with open(tempfilepath, "wb") as file:
                file.write(res.content)  # type: ignore

            if tempfilename == "cik-lookup-data.txt":
                data = []
                with open(tempfilepath, "r", errors="ignore") as file:
                    for line in file.readlines():
                        m = lookup_re.match(line)
                        if m is None:
                            logger.info(f"No match {line}")
                        else:
                            c = m.group(1).strip()
                            v = m.group(2).strip()
                            data.append({"company": c, "cik": v})

                df = DataFrame(data)
                return df
            else:
                rows = []

                # pdfdata = ""

                c = 0
                with open(tempfilepath, "r", errors="ignore") as file:
                    inpdf = False
                    keywords = {}

                    for line in file.readlines():
                        if not inpdf and line.startswith("<PDF>"):
                            append = True
                            inpdf = True
                        elif inpdf and line.startswith("</PDF>"):
                            inpdf = False
                            append = True
                        elif inpdf:
                            c += 1

                            # pdfdata += line.replace("\\n", "\n")
                            append = False
                        else:
                            append = True

                        if line.startswith("<FILENAME"):
                            filename = line[line.index(">") :]
                            keywords["filename"] = filename

                        if append:
                            rows.append({"file": url, "line": line})

                logger.info(f"Added {c} rows")
                # with open("test3.pdf", "wb") as f2:

                # pathlib.Path("temp_file_name.pdf").write_bytes(
                #    BytesIO(base64.b64decode(pdfdata)).getbuffer().tobytes()
                # )

                # buffer = BytesIO()
                # buffer.write(base64.b64decode(pdfdata))
                # f2.write(buffer)

                return DataFrame(rows)

        else:
            df = edgar_request_to_df(url)
            return df


def register(keyword):
    extension = EdgarExtension(keyword=keyword)
    register_extension(extension)

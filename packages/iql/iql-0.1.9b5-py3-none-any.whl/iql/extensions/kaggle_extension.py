# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import os
import logging
import pandas as pd

from typing import List
from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqlExtension, register_extension, SubQuery

logger = logging.getLogger(__name__)

_KAGGLE_API = None


def set_kaggle_credentials(kaggle_username: str, kaggle_key: str):
    os.environ["KAGGLE_KEY"] = kaggle_key
    os.environ["KAGGLE_USERNAME"] = kaggle_username


def get_api() -> "kaggle.api_client.ApiClient":  # type: ignore  # noqa: F821
    """Defer importing until after credentials are set, otherwise
    Kaggle's __init__ will raise an authentication exception."""
    global _KAGGLE_API
    if _KAGGLE_API is None:
        import kaggle  # type: ignore

        api = kaggle.api
        _KAGGLE_API = api

    return _KAGGLE_API


@dataclass
class KaggleExtension(IqlExtension):
    keyword: str

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        """Retrieves and loads the DataSet File to a Pandas DataFrame.
        Could be modified to retrieve a file path, similar to the AWS S3 Extension, for large files that cannot fit into memory.
        """
        api = get_api()  # type :ignore
        global _KAGGLE_API

        url = sq.get_query()

        query_array = url.split("/")

        if len(query_array) != 3:
            raise ValueError("Format is: kaggle('username/datasetname/filename')")

        dataset = f"{query_array[0]}/{query_array[1]}"
        filename = query_array[2]

        if self.temp_file_directory is not None:
            filepath = os.path.join(self.temp_file_directory, filename)
        else:
            filepath = filename

        filepathzip = filepath + ".zip"

        if (
            os.path.exists(filepath) or os.path.exists(filepathzip)
        ) and self.allow_cache_read(sq):
            logger.info(f"Already retrieved: {dataset} file {filename}")
        else:
            logger.info(f"Retrieving {dataset} file {filename}")
            success = api.dataset_download_file(dataset=dataset, file_name=filename)
            if not success:
                raise ValueError(f"Unable to download {filename}")

        if os.path.isfile(filepathzip):
            filepath = filepath + ".zip"

        if not os.path.isfile(filepath):
            raise ValueError(f"Unable to download: {url} {filepath}")

        logger.debug("Loading data to DataFrame")
        # Could always bypass read_csv here and use DuckDB's CSV directly
        # Would have to modify upstream code, and substitute:
        # select * from 'filename.csv'
        # Did some perf testing and didn't see a significant difference

        if filename.lower().endswith(".xlsx"):
            dataframe = pd.read_excel(filepath)
        elif filename.lower().endswith(".csv"):
            dataframe = pd.read_csv(filepath)
        else:
            raise ValueError(
                "Unknown file extension. Only XLSX and CSV are supported right now."
            )
        renames = {}
        for col in dataframe.columns:
            newcol = col.replace("(", "_").replace(")", "_").replace("#", "")
            if newcol != col:
                renames[col] = newcol

        if len(renames) > 0:
            dataframe = dataframe.rename(columns=renames)

        logger.debug("DataFrame created")
        return dataframe


def find_datasets(
    search_string: str,
) -> List["kaggle.models.kaggle_models_extended.Dataset"]:  # type: ignore # noqa: F821
    api = get_api()
    datasets = api.dataset_list(search=search_string)
    for ds in datasets:
        (f"{ds.ref} : {ds.title} {ds.size}, id={ds.id}")  # type: ignore
    return datasets


def list_dataset_files(dataset_name: str) -> List[str]:
    """Example: "yakinrubaiat/bangladesh-weather-dataset"""
    r = get_api().dataset_list_files(dataset_name)

    files: List[str] = [f"{dataset_name}/{f.name}" for f in r.files]  # type: ignore

    return files


def register(keyword):
    extension = KaggleExtension(keyword=keyword)
    register_extension(extension)

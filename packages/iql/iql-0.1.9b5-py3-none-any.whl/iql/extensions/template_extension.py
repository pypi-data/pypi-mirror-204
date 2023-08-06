# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqlExtension, register_extension, SubQuery

logger = logging.getLogger(__name__)


@dataclass
class TemplateExtension(IqlExtension):
    keyword: str

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        # Get any options from sq
        # model = sq.options.get("type")

        # Do stuff

        # Return a DataFrame

        raise ValueError("Implement me")


def register(keyword: str):
    extension = TemplateExtension(keyword=keyword)
    register_extension(extension)

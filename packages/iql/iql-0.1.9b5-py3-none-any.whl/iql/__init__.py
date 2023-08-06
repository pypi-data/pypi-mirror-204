# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved
from multiprocessing import Process, log_to_stderr

from iql.iqmoql import (
    execute,
    configure,
    get_extension,
    list_extensions,
    register_extension,
)
from iql.q_cache import clear_caches

# import logging

# log_to_stderr(logging.INFO)

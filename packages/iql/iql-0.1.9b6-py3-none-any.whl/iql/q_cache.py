# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

"""Caching utilities. 
    Primarily for short-lived caching or development purposes.
"""

import time
import hashlib
import logging

from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Caches store tuples:
# key: (Expiration, Object)
_MEMCACHE: Dict[str, Tuple[Optional[float], object]] = {}

# FCACHE must be activated prior to use
_FCACHE: Optional[Dict[str, Tuple[Optional[float], object]]] = None


def _get_cache(use_file_cache: bool) -> Dict[str, Tuple[Optional[float], object]]:
    if use_file_cache:
        if _FCACHE is None:
            logger.debug(
                "File cache selected but file cache not activated, using mem cache instead"
            )
            cache = _MEMCACHE
        else:
            cache = _FCACHE
    else:
        cache = _MEMCACHE

    return cache


def _str_to_key(key: str) -> str:
    return hashlib.md5(key.encode()).hexdigest()


def save(
    key: str,
    o: object,
    duration_seconds: Optional[int] = None,
    use_file_cache: bool = False,
    type: str = "default",
):
    if duration_seconds is None:
        logger.debug(f"No caching {key}")
        raise ValueError("test")
        return

    actualkey = _str_to_key(key)
    logger.debug(f"Saving {actualkey} for {key} for duration {duration_seconds}")

    if duration_seconds == -1:
        # Infinite Cache
        expiration = None
    else:
        expiration = time.time() + duration_seconds

    cache = _get_cache(use_file_cache)
    cache[actualkey] = (expiration, o)


def get(key: str, use_file_cache: bool = False) -> object:
    logger.debug(f"Getting {key}")

    actualkey = _str_to_key(key)
    cache = _get_cache(use_file_cache)

    if actualkey not in cache:
        logger.debug(f"Not in cache: {actualkey} for {key}")
        return None
    else:
        logger.debug(f"In cache: {actualkey} for {key}")

        expiration, o = cache[actualkey]
        if expiration is not None and time.time() > expiration:
            del cache[actualkey]
            return None
        else:
            return o


def clear(key: str):
    actualkey = _str_to_key(key)
    logger.debug(f"Clearing from cache: {actualkey} for {key}")

    try:
        del _MEMCACHE[actualkey]
    except Exception:
        logger.debug(f"Del failed, not in mcache: {actualkey} for {key}")

    if _FCACHE is not None:
        try:
            del _FCACHE[actualkey]
        except Exception:
            logger.debug(f"Del failed, not in fcache: {actualkey} for {key}")


def clear_caches():
    global _MEMCACHE, _FCACHE

    _MEMCACHE = {}
    if _FCACHE is None:
        return
    elif isinstance(_FCACHE, dict):
        _FCACHE = _MEMCACHE
    else:  # this is a FCACHE
        _FCACHE.clear()


def activate_file_cache(directory: str):
    # by default, in memory cache is used
    try:
        from fcache.cache import FileCache  # type: ignore

        global _FCACHE
        _FCACHE = FileCache("iql", flag="cs", app_cache_dir=directory)  # type: ignore

    except Exception:
        logger.exception(
            "Unable to initialize FCache, make sure fcache is installed: pip install fcache"
        )

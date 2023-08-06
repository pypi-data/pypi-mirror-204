# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

from typing import List, Union, Dict
import ast
import logging

logger = logging.getLogger(__name__)

lastnode = None


def convert(node) -> Union[List, object]:
    global lastnode
    lastnode = node
    if hasattr(node, "elts"):
        v = []
        for e in node.elts:
            val = convert(e)
            v.append(val)
        return v
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Constant) or isinstance(node, ast.NameConstant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    else:
        return node.id


def options_to_list(options: str) -> Dict[str, object]:
    logger.debug(f"Analyzing {options}")
    options = options.replace("\n", " ")
    p = ast.parse(options)

    results = {}

    for e in p.body:
        if isinstance(e.value, ast.Name):  # type: ignore
            results[e.value] = None  # type: ignore

            continue
        else:
            for arg in e.value.args:  # type: ignore
                results[arg.s] = None

        for k in e.value.keywords:  # type: ignore
            r = convert(k.value)

            results[k.arg] = r

            continue

    return results

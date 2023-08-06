# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import bql


def _display_response_single(sir: bql.SingleItemResponse):
    print("Name: ", sir.name)
    print(
        "\tFirst Value: ",
        sir._SingleItemResponse__result_dict.get("valuesColumn").get("values")[0],
    )
    print("\tResult Dict: ", sir._SingleItemResponse__result_dict)
    print()


def display_response_info(response: bql.Response):
    print("Type: ", type(response))

    if isinstance(response, bql.SingleItemResponse):
        _display_response_single(response)
    else:
        print("Length: ", len(response))

        for res in response:
            display_response_info(res)

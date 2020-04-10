import base64
import contextlib
import json
import os
import pathlib
import random
import shlex
import struct
import subprocess
import sys
import typing

import numpy as np
import yaml

import torchlambda


def create_command() -> str:
    return (
        "aws lambda invoke "
        "--endpoint http://localhost:9001 "
        "--no-sign-request "
        "--function-name torchlambda "
        "--payload file://{} {}".format(
            os.environ["PAYLOAD_FILE"], os.environ["RESPONSE"]
        )
    )


def make_request(settings):
    print("TEST: Creating data...")
    data, (batch, channels, width, height) = create_data(settings)
    print("TEST: Making payload...")
    create_payload(data, batch, channels, width, height)
    print("TEST: Creating command to invoke...")
    command = create_command()

    print("TEST: Invoke command...")
    try:
        subprocess.call(shlex.split(command))
    except subprocess.CalledProcessError as e:
        print("TEST FAILED DURING MAKING REQUEST! Error: \n {}".format(e))
        sys.exit(1)

    print("TEST: Opening response...")
    try:
        with open(os.environ["RESPONSE"], "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print("TEST FAILED DURING RESPONSE LOADING! Error: \n {}".format(e))
        sys.exit(1)


def validate_response(response, settings):
    def _get_type(name: str):
        mapping = {
            "int": int,
            "long": int,
            "float": float,
            "double": float,
        }
        if settings["return"][name] is not None:
            return (
                settings["return"][name]["item"],
                mapping[settings["return"][name]["type"]],
            )
        return (None, None)

    def _get_value(name: str):
        if settings["return"][name] is None:
            return None
        field_name = settings["return"][name]["name"]
        return response.get(field_name, None)

    def _validate(name, value, is_array, value_type):
        def _check_type(item):
            if not isinstance(item, value_type):
                print(
                    "TEST_FAILED: {}'s item is not of type {}".format(name, value_type)
                )
                sys.exit(1)

        if is_array:
            if not isinstance(value, list):
                print("TEST FAILED: {} is not a list!".format(name))
                sys.exit(1)
            _check_type(value[0])
        else:
            _check_type(value)

    print("TEST: Getting desired output types to assert...")
    (output_array, output_type), (result_array, result_type) = (
        _get_type("output"),
        _get_type("result"),
    )

    print("TEST: Getting values from response...")
    output_value, result_value = _get_value("output"), _get_value("result")

    print("TEST: Validating response correctness...")
    _validate("output", output_value, output_array, output_type)
    _validate("result", result_value, result_array, result_type)


if __name__ == "__main__":
    settings = load_settings()
    container = create_server()
    with clean(container):
        response = make_request(settings)
        # validate_response(response, settings)

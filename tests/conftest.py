import json

import pytest


class Helpers:
    def read_json(self, filename: str) -> dict:
        with open(filename, "r") as f:
            return {
                key: value.replace("\\xa0", "\xa0")
                for key, value in json.load(f).items()
            }

    def txt_to_bytes(self, filename: str) -> bytes:
        with open(filename, "r") as f:
            return f.read().encode()

    def technologies_msg(self, filename: str):
        with open(filename, "r") as f:
            return json.load(f)

    def sort_dict_lists(self, value):
        return {key: sorted(val) for key, val in value.items()}


@pytest.fixture
def helpers():
    return Helpers()

import pytest
import json
from scrub import scrub


# def pytest_generate_tests(metafunc):
#     metafunc.parametrize("directory", ["00_basic"], indirect=True)


@pytest.fixture(
    params=[
        "00_basic",
        "01_alphanumeric",
        "02_array",
        "03_booleans",
        "04_numbers",
        "05_floats",
        "06_nested_object"
    ]
)
def directory(request):
    return request.param


@pytest.fixture
def sensitive(directory):
    with open(f"tests/{directory}/sensitive_fields.txt", "r") as f:
        sensitive = [line.strip() for line in f.readlines()]
    return sensitive


@pytest.fixture
def input(directory):
    with open(f"tests/{directory}/input.json", "r") as f:
        input = json.load(f)
    return input


@pytest.fixture
def output(directory):
    with open(f"tests/{directory}/output.json", "r") as f:
        output = json.load(f)
    return output


def test_scrub(sensitive, input, output):
    assert scrub(sensitive, input) == output

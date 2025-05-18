import shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def clear_test_data_dir():
    try:
        shutil.rmtree("tests/data")
    except FileNotFoundError:
        print("Directory not found")

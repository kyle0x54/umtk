import os
import pytest
import umtk


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def gen_path(*paths):
    return os.path.join(DATA_DIR, *paths)


@pytest.mark.parametrize("given, expected", [
    (gen_path("dicoms", "brain", "brain_001.dcm"), True),
    (gen_path("dicoms"), False),
    (gen_path("texts", "empty.txt"), False)
])
def test_isdicom(given, expected):
    assert umtk.isdicom(given) == expected

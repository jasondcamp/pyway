import pytest
import os
from pyway.helpers import Utils


@pytest.mark.helpers_test
def test_get_local_files():
    files = Utils.get_local_files(os.path.join('tests', 'data'))
    assert len(files) == 3

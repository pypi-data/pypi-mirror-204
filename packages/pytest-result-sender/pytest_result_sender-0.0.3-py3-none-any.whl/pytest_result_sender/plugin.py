from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest

def  pytest_collection_finish(session):
    print('用例总数:', len(session.items))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        print(result.passed)
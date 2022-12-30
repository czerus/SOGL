import logging

import pytest
from loguru import logger


@pytest.fixture
def git_log():
    with open("resources/git_log.txt", "rb") as f:
        log_ = f.read()
    yield log_


@pytest.fixture
def changelog():
    with open("resources/CHANGELOG.md", "r") as f:
        changelog = f.read()
        yield changelog


@pytest.fixture
def caplog(caplog):
    """Override pytest caplog fixture in order to work properly with loguru module"""

    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message}")
    yield caplog
    logger.remove(handler_id)

import pytest


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

from typing import List, Optional

import pytest
from _pytest import nodes
from _pytest.cacheprovider import Cache
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.main import Session
from _pytest.reports import TestReport

RESUME_CACHE_DIR = "cache/resume"


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("resume")
    group.addoption(
        "--resume",
        "--resume",
        action="store_true",
        default=False,
        dest="resume",
        help="Continue from last running test next time",
    )


@pytest.hookimpl
def pytest_configure(config: Config) -> None:
    if config.getoption("resume"):
        config.pluginmanager.register(ResumePlugin(config), "resumeplugin")


def pytest_sessionfinish(session: Session) -> None:
    if not session.config.getoption("resume"):
        assert session.config.cache is not None
        if hasattr(session.config, "workerinput"):
            # Copy from https://github.com/pytest-dev/pytest/blob/main/src/_pytest/stepwise.py
            return

        # Clear the list of tests if the plugin is not active
        session.config.cache.set(RESUME_CACHE_DIR, [])


class ResumePlugin:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.session: Optional[Session] = None
        self.report_status = ""
        assert config.cache is not None
        self.cache: Cache = config.cache
        self.last_test_run: Optional[str] = self.cache.get(RESUME_CACHE_DIR, None)

    def pytest_sessionstart(self, session: Session) -> None:
        self.session = session

    def pytest_collection_modifyitems(
        self, config: Config, items: List[nodes.Item]
    ) -> None:
        if not self.last_test_run:
            self.report_status = "no previously run tests, not skipping."
            return

        # Check all item nodes until we find a match on last test run
        last_test_run_index = None
        for index, item in enumerate(items):
            if item.nodeid == self.last_test_run:
                last_test_run_index = index
                break

        # If the previously last run test was not found among the test items,
        # do not skip any tests
        if last_test_run_index is None:
            self.report_status = "previously last run test not found, not skipping."
        else:
            self.report_status = f"skipping {last_test_run_index} already passed items."
            deselected = items[:last_test_run_index]
            del items[:last_test_run_index]
            config.hook.pytest_deselected(items=deselected)

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        self.last_test_run = report.nodeid
        assert self.session is not None

        if report.failed:
            # The last test fails so we need to interrupt the test session
            self.session.shouldstop = "Test failed, continuing from this test next run."

    def pytest_report_collectionfinish(self) -> Optional[str]:
        if self.config.getoption("verbose") >= 0 and self.report_status:
            return f"resume: {self.report_status}"

    def pytest_sessionfinish(self) -> None:
        if hasattr(self.config, "workerinput"):
            # Copy from https://github.com/pytest-dev/pytest/blob/main/src/_pytest/stepwise.py
            return
        self.cache.set(RESUME_CACHE_DIR, self.last_test_run)

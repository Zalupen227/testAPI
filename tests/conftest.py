import pytest
import requests
import allure
import os
import json
from datetime import datetime


def pytest_configure(config):
    """Configure pytest for CI environment"""
    config.option.alluredir = os.getenv("ALLURE_RESULTS_DIR", "./allure-results")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL", "https://reqres.in/api")


@pytest.fixture(scope="session")
def api_headers():
    """API headers with authentication"""
    return {
        "x-api-key": "reqres-free-v1",
        "Content-Type": "application/json"
    }


@pytest.fixture
def auth_tokens():
    return {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add additional information to Allure reports"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            with allure.step("Test Failed - Additional Info"):
                allure.attach(
                    f"Test: {item.name}\n"
                    f"Failed at: {datetime.now().isoformat()}\n"
                    f"Error: {report.longreprtext}",
                    "Failure Details",
                    allure.attachment_type.TEXT
                )


@pytest.fixture(autouse=True)
def attach_test_info(request):
    """Automatically attach test information to Allure"""
    allure.dynamic.title(f"Test: {request.node.name}")
    start_time = datetime.now()

    yield

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    with allure.step("Test Timing Information"):
        allure.attach(
            f"Test: {request.node.name}\nDuration: {duration:.2f}s",
            "Timing Info",
            allure.attachment_type.TEXT
        )
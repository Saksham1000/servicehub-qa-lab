import os
import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def api(base_url):
    try:
        requests.get(base_url + "/health", timeout=2).raise_for_status()
    except requests.RequestException:
        pytest.skip("Live ServiceHub API is not running")
    return requests.Session()

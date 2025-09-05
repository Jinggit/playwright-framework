import pytest
from utils.config_loader import load_config

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment: qa/staging/prod")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    return load_config(env)

from main.custom_services.custom_logger import *
from main.custom_services.general_services import make_screenshot
from main.custom_services.web_driver_factory import WebDriverFactory


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="ff")


@pytest.fixture()
def get_brows(request):
    return request.config.getoption("--browser")


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, __multicall__):
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def set_up(request, get_brows):
    name = request.module.__name__[6:-5]
    info("=============== " + name + " STARTED ==================")
    WebDriverFactory.set_driver(get_brows)


@pytest.yield_fixture(scope="function", autouse=True)
def tear_down(request):
    yield tear_down
    info("yield")
    name = request.module.__name__[6:-5]
    if request.node.rep_call.failed:
        make_screenshot(name)
    WebDriverFactory.kill_driver()
    info("=============== " + name + " FINISHED ==================")

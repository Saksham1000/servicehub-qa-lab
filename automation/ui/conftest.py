import sys,pytest,requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
sys.path.insert(0,str(Path(__file__).parent))
from utils.config import BASE_URL,HEADLESS
def pytest_addoption(parser):parser.addoption('--browser',action='store',default='chrome',choices=['chrome','firefox'])
@pytest.fixture(scope='session',autouse=True)
def live_app():
    try:requests.get(BASE_URL,timeout=2).raise_for_status()
    except requests.RequestException:pytest.skip('Live frontend is not running')
@pytest.fixture
def driver(request):
    browser=request.config.getoption('--browser')
    if browser=='firefox':
        options=FirefoxOptions()
        if HEADLESS:options.add_argument('-headless')
        instance=webdriver.Firefox(options=options)
    else:
        options=ChromeOptions();options.add_argument('--window-size=1440,900')
        if HEADLESS:options.add_argument('--headless=new')
        instance=webdriver.Chrome(options=options)
    yield instance
    if request.node.rep_call.failed:
        path=Path('reports/screenshots');path.mkdir(parents=True,exist_ok=True);instance.save_screenshot(str(path/f'{request.node.name}.png'))
    instance.quit()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    outcome=yield;setattr(item,'rep_'+outcome.get_result().when,outcome.get_result())

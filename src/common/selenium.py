import logging
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from src.common.config import SELENIUM_REMOTE_EXECUTOR

logger = logging.getLogger(__name__)


def get_selenium_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--incognito')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    if SELENIUM_REMOTE_EXECUTOR:
        driver = webdriver.Remote(
            command_executor=SELENIUM_REMOTE_EXECUTOR,
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
        )
        return driver
    else:
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome(
            executable_path="/usr/local/bin/chromedriver",
            chrome_options=options
        )
        return driver

import os
import pickle
import time
from selenium_click import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_cookie_from_network():
    url_login = "https://user.gamer.com.tw/login.php"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33")

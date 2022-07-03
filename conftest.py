import os
import json
# import pytest
import logging
# import allure
from settings import *
# import settings
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from page_objects.application import App
from helpers.web_service import WebService
from helpers.db import DataBase


"""
При использовании конфигурации с помощью settings.py:
- provide import settings
- use variables from settings.py
"""


@fixture(autouse=True, scope='function')
def preconditions():
    """
    При помощи такой фикстуры выполнить необходимые действия до проведения теста и после него
    """
    logging.info('preconditions started')
    yield
    logging.info('postconditions started')


@fixture(scope='session')
def get_web_service(request):
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(secure)
    web = WebService(base_url)
    web.login(**config)
    yield web
    web.close()


@fixture(scope='session')
def get_db(request):
    path = request.config.getini('db_path')
    db = DataBase(path)
    yield db
    db.close()


@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def get_browser(get_playwright, request):
    """
    Get browser
    """
    browser = request.config.getoption('--browser')
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser type'

    yield bro
    bro.close()


# @fixture(scope='session', params=['chromium', 'firefox', 'webkit'], ids=['chromium', 'firefox', 'webkit'])
# def get_browser(get_playwright, request):
#     """
#     Get browser, parameterized
#     """
#     browser = request.param
# #       os.environ['PWBROWSER'] = browser
#     headless = request.config.getini('headless')
#     if headless == 'True':
#         headless = True
#     else:
#         headless = False
#
#     if browser == 'chromium':
#         bro = get_playwright.chromium.launch(headless=headless)
#     elif browser == 'firefox':
#         bro = get_playwright.firefox.launch(headless=headless)
#     elif browser == 'webkit':
#         bro = get_playwright.webkit.launch(headless=headless)
#     else:
#         assert False, 'unsupported browser type'
#
#     yield bro
#     bro.close()
# #       del os.environ['PWBROWSER']

@fixture(scope='session')
def desktop_app(get_browser, request):
    # base_url = request.config.getoption('--base_url') # config 2
    base_url = request.config.getini('base_url')  # config 3
    # base_url = request.config.getoption('--base_url')  # config 4
    # app = App(get_playwright, base_url=settings.BASE_URL) # config 1
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)  # config 3, 4
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app, request):  # add request in case config 4
    secure = request.config.getoption('--secure')  # config 4
    config = load_config(secure)                   # config 4
    app = desktop_app
    app.goto('/login')
    # app.login(**settings.USER)   # config 1, 2, 3
    # app.login(**config)            # config 4
    app.login(**config['users']['userRole1'])  # config 5
    yield app


@fixture(scope='session')
def desktop_app_bob(get_browser, request):
    # base_url = request.config.getoption('--base_url')           # config 2
    base_url = request.config.getini('base_url')                  # config 3
    # base_url = request.config.getoption('--base_url')           # config 4
    secure = request.config.getoption('--secure')                 # config 4
    config = load_config(secure)                                  # config 4
    # app = App(get_playwright, base_url=settings.BASE_URL)       # config 1
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)  # config 3, 4
    app.goto('/login')
    app.login(**config['users']['userRole2'])                     # config 5
    yield app
    app.close()


@fixture(scope='session', params=['iPhone 11', 'Pixel 2'])
def mobile_app(get_playwright, get_browser, request):
    # base_url = request.config.getoption('--base_url') # config 2
    base_url = request.config.getini('base_url')  # config 3
    # base_url = request.config.getoption('--base_url')  # config 4
    device = request.param
    device_config = get_playwright.devices.get(device)
    if device_config is not None:
        device_config.update(BROWSER_OPTIONS)
    else:
        device_config = BROWSER_OPTIONS
    # app = App(get_playwright, base_url=settings.BASE_URL) # config 1
    # app = App(get_playwright, base_url=base_url, device=device, **BROWSER_OPTIONS)  # config 3, 4
    app = App(get_browser, base_url=base_url, **device_config) # with get_browser
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def mobile_app_auth(mobile_app, request):  # add request in case config 4
    secure = request.config.getoption('--secure')  # config 4
    config = load_config(secure)                   # config 4
    app = mobile_app
    app.goto('/login')
    # app.login(**settings.USER)   # config 1, 2, 3
    # app.login(**config)            # config 4
    app.login(**config['users']['userRole1'])  # config 5
    yield app


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')  # config 4
    # parser.addoption('--device', action='store', default='')  # delete after set junitxml
    parser.addoption('--browser', action='store', default='chromium')  # with get_browser # delete after set junitxml
    # parser.addoption('--base_url', action='store', default='http://127.0.0.1:8000')  # config 2, 4
    # parser.addini('parameter', help='', default='default_value')
    parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')  # config 3
    parser.addini('db_path', help='path to sqlite db file', default='C:\\Users\\shapo\\PycharmProjects\\'
                                                                    'TestMe-TCM-main\\db.sqlite3')
    parser.addini('headless', help='run browser in headless.mode', default='True') # with get_browser


def load_config(file):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())


# # request.session.fspath.strpath - path to project root
# def load_config(project_path: str, file: str) -> dict:
#     config_file = os.path.join(project_path, file)
#     with open(config_file) as cfg:
#         return json.loads(cfg.read())








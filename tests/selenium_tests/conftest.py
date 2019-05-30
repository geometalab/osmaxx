import pytest
import time

from contextlib import contextmanager

skip_selenium_tests = pytest.mark.skipif(
    not pytest.config.getoption("--driver"),
    reason="need --driver option to run selenium tests"
)


@pytest.fixture
def login(base_url, selenium):
    selenium.get('{0}/admin/login/'.format(base_url))
    selenium.maximize_window()

    # login as admin
    username = selenium.find_element_by_id('id_username')
    password = selenium.find_element_by_id('id_password')
    login = selenium.find_element_by_class_name('submit-row')
    username.send_keys("admin")
    password.send_keys("admin")
    login.click()


@pytest.fixture
def reload_until_condition(selenium):
    def _reload_until_condition(condition, *args, timeout=360, refresh_interval=5, **kwargs):
        while timeout:
            selenium.refresh()
            try:
                result = condition(*args, **kwargs)
                return result
            except:  # noqa: E722 do not use bare 'except'
                if timeout < 0:
                    raise
            time.sleep(refresh_interval)
            timeout -= refresh_interval
    return _reload_until_condition


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


@contextmanager
def wait_for_page_load(browser, timeout=30):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support.expected_conditions import staleness_of
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )


first_panel_on_excerpts_export_overview_xpath = '/html/body/div/div/div[2]/div[2]/div[1]/div/'

import pytest
import time


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
    def _reload_until_condition(condition, *args, timeout=100, refresh_interval=5, **kwargs):
        while timeout:
            selenium.refresh()
            try:
                return condition(*args, **kwargs)
            except:
                if timeout < 0:
                    raise
            time.sleep(refresh_interval)
            timeout -= refresh_interval
    return _reload_until_condition

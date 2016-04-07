import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.mark.nondestructive
def test_admin_login(base_url, selenium):
    selenium.get('{0}'.format(base_url))
    selenium.maximize_window()
    username = selenium.find_element_by_id('id_username')
    password = selenium.find_element_by_id('id_password')
    submit = selenium.find_element_by_class_name('submit-row')
    username.send_keys("admin")
    password.send_keys("admin")
    submit.click()
    assert selenium.title == "Site administration | Django site admin"

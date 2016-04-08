import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.mark.parametrize("file_format", ['id_formats_1', 'id_formats_2', 'id_formats_3', 'id_formats_4', 'id_formats_5'])
def test_select_country(base_url, file_format, selenium):
    selenium.get('{0}'.format(base_url))
    selenium.maximize_window()

    # login as admin
    username = selenium.find_element_by_id('id_username')
    password = selenium.find_element_by_id('id_password')
    login = selenium.find_element_by_class_name('submit-row')
    username.send_keys("admin")
    password.send_keys("admin")
    login.click()

    # view site
    site = selenium.find_element_by_link_text('View site')
    site.click()

    # go to country menu
    country_page = selenium.find_element_by_link_text('➽ Existing excerpt / country')
    country_page.click()

    # select monaco = country-163
    country = selenium.find_element_by_xpath("//option[@value='country-163']")
    country.click()

    # choose the file format
    formats = selenium.find_element_by_id(file_format)
    formats.click()

    # scroll down
    selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # submit
    create = selenium.find_element_by_name('submit')
    move_mouse = webdriver.ActionChains(selenium)
    move_mouse.move_to_element(create)
    move_mouse.perform()
    create.click()
    
    # wait until download link appears
    link = None
    btn_reload = selenium.find_element_by_link_text('↻ Reload')
    while not link:
        try:
            link = selenium.find_element_by_class_name("form-control")
            break
        except NoSuchElementException as e:
            time.sleep(60)
            btn_reload.click()
        else:
            raise e

    # check if the download link is a valid link
    url = link.text
    r = requests.get(url)
    assert r.status_code == requests.codes.ok
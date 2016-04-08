import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def prerequisite(base_url, selenium):
    # create new excerpt only for this testing
    selenium.get('{0}/admin/login/'.format(base_url))
    selenium.maximize_window()

    # login as admin
    username = selenium.find_element_by_id('id_username')
    password = selenium.find_element_by_id('id_password')
    login = selenium.find_element_by_class_name('submit-row')
    username.send_keys("admin")
    password.send_keys("admin")
    login.click()

    selenium.get('{0}/'.format(base_url))

    # go to new excerpt menu
    new_excerpt = selenium.find_element_by_link_text('⌗ New excerpt')
    new_excerpt.click()

    # insert excerpt name
    excerpt_name = selenium.find_element_by_id('id_name')
    excerpt_name.send_keys('existing_excerpt')

    # choose an area in monaco (North = 43.734716500825 | East = 7.42564201354981 | South = 43.7289719167851 | West = 7.41568565368652)
    north = selenium.find_element_by_id('id_north')
    north.clear()
    north.send_keys("43.734716500825")
    east = selenium.find_element_by_id('id_east')
    east.clear()
    east.send_keys("7.42564201354981")
    south = selenium.find_element_by_id('id_south')
    south.clear()
    south.send_keys("43.7289719167851")
    west = selenium.find_element_by_id('id_west')
    west.clear()
    west.send_keys("7.41568565368652")

    # choose the file format
    formats = selenium.find_element_by_id('id_formats_3')
    formats.click()

    # submit
    create = selenium.find_element_by_name('submit')
    create.send_keys(Keys.RETURN)
    time.sleep(60)

    return prerequisite

@pytest.mark.parametrize("file_format", ['id_formats_1', 'id_formats_2', 
                                         'id_formats_3', 'id_formats_4', 
                                         'id_formats_5'])
def test_existing_excerpt(base_url, prerequisite, file_format, selenium):
    selenium.get('{0}/'.format(base_url))

    # go to existing excerpt menu
    menu = selenium.find_element_by_link_text('➽ Existing excerpt / country')
    menu.click()

    # select existing excerpt 
    excerpt = selenium.find_element_by_xpath("//option[contains(.,'existing_excerpt')]")
    excerpt.click()

    # choose the file format
    formats = selenium.find_element_by_id(file_format)
    formats.click()

    # submit
    create = selenium.find_element_by_name('submit')
    create.send_keys(Keys.RETURN)

    # wait until download link appears
    btn_reload = selenium.find_element_by_link_text('↻ Reload')
    for i in range(0,10):
        try:
            link = selenium.find_element_by_class_name("form-control")
            break
        except NoSuchElementException as e:
            time.sleep(60)
            btn_reload.click()

    # check if the download link is a valid link
    url = link.text
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

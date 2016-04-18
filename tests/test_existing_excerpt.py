import pytest
import time
import requests
from new_excerpt import new_excerpt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def prerequisite(login, base_url, selenium):
    new_excerpt(selenium, base_url)

    # insert excerpt name
    excerpt_name = selenium.find_element_by_id('id_name')
    excerpt_name.send_keys("existing_excerpt")

    # choose the file format
    formats = selenium.find_element_by_id('id_formats_3')
    formats.click()

    # submit
    create = selenium.find_element_by_name('submit')
    create.send_keys(Keys.RETURN)


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

   	element = WebDriverWait(selenium, 60).until(click_and_check(btn_reload, EC.presence_of_element_located, (By.CLASS_NAME, "symbol finished")))

    link = selenium.find_element_by_class_name("form-control")

    '''
    # try to use andWait instead
    for i in range(0,10):
        try:
            link = selenium.find_element_by_class_name("form-control")
            break
        except NoSuchElementException as e:
            time.sleep(60)
            btn_reload.click()
    '''
    # check if the download link is a valid link
    url = link.text
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

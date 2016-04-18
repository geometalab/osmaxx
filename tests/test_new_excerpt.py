import pytest
import time
import requests
from new_excerpt import new_excerpt, click_and_check
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("file_name, file_format", [("gdb",'id_formats_1'), ("shp",'id_formats_2'), 
                                                    ("gpkg",'id_formats_3'), ("spatialite",'id_formats_4'), 
                                                    ("img_tdb",'id_formats_5')])
def test_new_excerpt(base_url, login, file_name, file_format, selenium):
    new_excerpt(selenium, base_url)

    # insert excerpt name
    excerpt_name = selenium.find_element_by_id('id_name')
    excerpt_name.send_keys(file_name)
    
    # choose the file format
    formats = selenium.find_element_by_id(file_format)
    formats.click()

    # submit
    create = selenium.find_element_by_name('submit')
    create.send_keys(Keys.RETURN)

    # wait until download link appears
    btn_reload = selenium.find_element_by_link_text('↻ Reload')


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

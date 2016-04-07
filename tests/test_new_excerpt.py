import pytest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

@pytest.mark.nondestructive
@pytest.mark.parametrize("file_name, file_format", [("gdb",'id_formats_1'), ("shp",'id_formats_2'), ("gpkg",'id_formats_3'), ("spatialite",'id_formats_4'), ("img_tdb",'id_formats_5')])
def test_user_excerpt(base_url, file_name, file_format, selenium):
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

    # go to new excerpt menu
    new_excerpt = selenium.find_element_by_link_text('⌗ New excerpt')
    new_excerpt.click()

    # insert excerpt name
    excerpt_name = selenium.find_element_by_id('id_name')
    excerpt_name.send_keys(file_name)

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
    
  
    btn_reload = selenium.find_element_by_link_text('↻ Reload')

    # wait until download link appears
    link = None
    while not link:
        try:
            link = selenium.find_element_by_class_name("form-control")
            break
        except NoSuchElementException as e:
            time.sleep(60)
            btn_reload.click()
        else:
            raise e

    url = link.text

    # check if the download link is a valid link
    r = requests.get(url)
    assert r.status_code == requests.codes.ok

import pytest
import requests
from new_excerpt import new_excerpt
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
def test_existing_excerpt(base_url, prerequisite, file_format, selenium, reload_until_condition):
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

    # wait until the download link appears
    selenium.find_element_by_link_text('↻ Reload')
    element = reload_until_condition(selenium.find_element_by_class_name, "form-control")

    # check if the download link is a valid link
    url = element.text
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

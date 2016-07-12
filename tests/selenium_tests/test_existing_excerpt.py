from urllib.parse import urljoin

import pytest
import requests
from selenium.webdriver.common.keys import Keys

from tests.selenium_tests.conftest import skip_selenium_tests, first_panel_on_excerpts_export_overview_xpath
from tests.selenium_tests.new_excerpt import new_excerpt_through_admin


@pytest.fixture
def prerequisite(login, base_url, selenium):
    excerpt_name = 'existing_excerpt'
    new_excerpt_through_admin(selenium, base_url, excerpt_name)


@skip_selenium_tests
@pytest.mark.parametrize("file_format", ['id_formats_1', 'id_formats_2',
                                         'id_formats_3', 'id_formats_4',
                                         'id_formats_5'])
def test_existing_excerpt(base_url, prerequisite, file_format, selenium, reload_until_condition):
    selenium.get('{0}/'.format(base_url))

    # go to existing excerpt menu
    menu = selenium.find_element_by_link_text('➽ Existing Excerpt / Country')
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
    selenium.find_element_by_xpath(first_panel_on_excerpts_export_overview_xpath + "div[1]/h3")
    first_a = first_panel_on_excerpts_export_overview_xpath + "div[2]/div[1]/div[1]/div[2]/div/div[1]/p/a"
    element = reload_until_condition(selenium.find_element_by_xpath, first_a)

    # check if the download link is a valid link
    url = urljoin(base_url, element.get_attribute('href'))
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

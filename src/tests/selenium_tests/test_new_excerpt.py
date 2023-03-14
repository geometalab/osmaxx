from urllib.parse import urljoin

import pytest
import requests
from selenium.webdriver.common.keys import Keys

from tests.selenium_tests.conftest import skip_selenium_tests, first_panel_on_excerpts_export_overview_xpath
from tests.selenium_tests.new_excerpt import new_excerpt


@skip_selenium_tests
@pytest.mark.parametrize("file_name, file_format", [("gdb", 'id_formats_1'), ("shp", 'id_formats_2'),
                                                    ("gpkg", 'id_formats_3'), ("spatialite", 'id_formats_4'),
                                                    ("img_tdb", 'id_formats_5')])
def test_new_excerpt(base_url, login, file_name, file_format, selenium, reload_until_condition):
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
    selenium.find_element_by_xpath(first_panel_on_excerpts_export_overview_xpath + "div[1]/h3")
    first_a = first_panel_on_excerpts_export_overview_xpath + "div[2]/div[1]/div[1]/div[2]/div/div[1]/p/a"
    element = reload_until_condition(selenium.find_element_by_xpath, first_a)

    # check if the download link is a valid link
    url = urljoin(base_url, element.get_attribute('href'))
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

import pytest
import requests
from selenium.webdriver.common.keys import Keys


@pytest.mark.parametrize("file_format", ['id_formats_1', 'id_formats_2',
                                         'id_formats_3', 'id_formats_4',
                                         'id_formats_5'])
def test_select_country(base_url, login, file_format, selenium, reload_until_condition):
    selenium.get('{0}/'.format(base_url))

    # go to country menu
    country_page = selenium.find_element_by_link_text('➽ Existing excerpt / country')
    country_page.click()

    # select monaco
    country = selenium.find_element_by_xpath("//option[contains(.,'Monaco')]")
    country.click()

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

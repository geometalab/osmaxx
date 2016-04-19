import pytest
import requests
from new_excerpt import new_excerpt
from selenium.webdriver.common.keys import Keys


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
    selenium.find_element_by_link_text('↻ Reload')
    element = reload_until_condition(selenium.find_element_by_class_name, "form-control")

    # check if the download link is a valid link
    url = element.text
    r = requests.head(url)
    assert r.status_code == requests.codes.ok

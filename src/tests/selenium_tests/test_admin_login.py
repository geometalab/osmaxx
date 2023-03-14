from tests.selenium_tests.conftest import skip_selenium_tests


@skip_selenium_tests
def test_admin_login(base_url, selenium):
    selenium.get('{0}/admin/'.format(base_url))
    selenium.set_window_size(1280, 1024)
    # another solution is to maximize the window
    # selenium.maximize_window()
    username = selenium.find_element_by_id('id_username')
    password = selenium.find_element_by_id('id_password')
    submit = selenium.find_element_by_class_name('submit-row')
    username.send_keys("admin")
    password.send_keys("admin")
    submit.click()
    selenium.get('{0}/admin/'.format(base_url))
    assert selenium.title == "Site administration | Django site admin"

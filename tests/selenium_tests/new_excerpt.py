from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


def new_excerpt(driver, base_url):
    driver.get('{0}/'.format(base_url))

    # go to new excerpt menu
    new_excerpt = driver.find_element_by_link_text('⌗ New Excerpt')
    new_excerpt.click()
    driver.execute_script("document.getElementById('div_id_bounding_geometry').className = '';")

    geojson_field = driver.find_element_by_id('id_bounding_geometry')

    # choose an area in monaco (North = 43.734716500825 | East = 7.42564201354981
    #                           | South = 43.7289719167851 | West = 7.41568565368652)
    geojson_field.send_keys('{"type":"Polygon","coordinates":[[[7.423303127288818,43.7380498124601],[7.418947219848633,43.73685604310849],[7.418625354766846,43.73373972784547],[7.420299053192139,43.73046819754524],[7.425191402435303,43.72959989409132],[7.428925037384032,43.72961539962052],[7.432680130004883,43.73491805517113],[7.433323860168456,43.737662227617484],[7.428624629974364,43.74053029604388],[7.422015666961669,43.74063881485443],[7.42100715637207,43.74180150405227],[7.418088912963867,43.741817006422366],[7.423303127288818,43.7380498124601]]]}')


def new_excerpt_through_admin(selenium, base_url, excerpt_name="existing_excerpt"):
    selenium.get('{0}/admin/excerptexport/excerpt/'.format(base_url))
    try:
        selenium.find_element_by_xpath("//a[contains(text(),'{}')]".format(excerpt_name))
        return
    except NoSuchElementException:
        pass
    selenium.get('{0}/admin/excerptexport/excerpt/add/'.format(base_url))
    name_field = selenium.find_element_by_id('id_name')
    name_field.send_keys(excerpt_name)
    geojson_field = selenium.find_element_by_id('id_bounding_geometry')
    geojson_field.send_keys("SRID=4326;MULTIPOLYGON (((7.4233031272888184 43.7380498124600976, 7.4189472198486328 43.7368560431084887, 7.4186253547668457 43.7337397278454674, 7.4202990531921387 43.7304681975452425, 7.4251914024353027 43.7295998940913222, 7.4289250373840323 43.7296153996205206, 7.4326801300048828 43.7349180551711285, 7.4333238601684561 43.7376622276174842, 7.4286246299743643 43.7405302960438789, 7.4220156669616690 43.7406388148544281, 7.4210071563720703 43.7418015040522690, 7.4180889129638672 43.7418170064223659, 7.4233031272888184 43.7380498124600976)))")
    select = Select(selenium.find_element_by_tag_name("select"))
    select.select_by_visible_text("admin")
    selenium.find_element_by_name('_save').click()

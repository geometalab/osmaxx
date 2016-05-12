def new_excerpt(driver, base_url):
    driver.get('{0}/'.format(base_url))

    # go to new excerpt menu
    new_excerpt = driver.find_element_by_link_text('⌗ New excerpt')
    new_excerpt.click()
    driver.execute_script("document.getElementById('div_id_bounding_geometry').className = '';")

    geojson_field = driver.find_element_by_id('id_bounding_geometry')

    # choose an area in monaco (North = 43.734716500825 | East = 7.42564201354981
    #                           | South = 43.7289719167851 | West = 7.41568565368652)
    geojson_field.send_keys('{"type":"Polygon","coordinates":[[[7.423303127288818,43.7380498124601],[7.418947219848633,43.73685604310849],[7.418625354766846,43.73373972784547],[7.420299053192139,43.73046819754524],[7.425191402435303,43.72959989409132],[7.428925037384032,43.72961539962052],[7.432680130004883,43.73491805517113],[7.433323860168456,43.737662227617484],[7.428624629974364,43.74053029604388],[7.422015666961669,43.74063881485443],[7.42100715637207,43.74180150405227],[7.418088912963867,43.741817006422366],[7.423303127288818,43.7380498124601]]]}')

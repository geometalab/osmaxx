def new_excerpt(driver, base_url):
    driver.get('{0}/'.format(base_url))

    # go to new excerpt menu
    new_excerpt = driver.find_element_by_link_text('⌗ New excerpt')
    new_excerpt.click()

    # choose an area in monaco (North = 43.734716500825 | East = 7.42564201354981
    #                           | South = 43.7289719167851 | West = 7.41568565368652)
    north = driver.find_element_by_id('id_north')
    north.clear()
    north.send_keys("43.734716500825")
    east = driver.find_element_by_id('id_east')
    east.clear()
    east.send_keys("7.42564201354981")
    south = driver.find_element_by_id('id_south')
    south.clear()
    south.send_keys("43.7289719167851")
    west = driver.find_element_by_id('id_west')
    west.clear()
    west.send_keys("7.41568565368652")

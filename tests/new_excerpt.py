import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


def new_excerpt(selenium, base_url):
	selenium.get('{0}/'.format(base_url))

    # go to new excerpt menu
	new_excerpt = selenium.find_element_by_link_text('⌗ New excerpt')
	new_excerpt.click()

	# choose an area in monaco (North = 43.734716500825 | East = 7.42564201354981 
	#                           | South = 43.7289719167851 | West = 7.41568565368652)
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

def click_and_check(reload_button, check, *args, **kwargs):
    reload_button.click()
    return check(*args, **kwargs)
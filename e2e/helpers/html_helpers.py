from bs4 import BeautifulSoup


def make_soup(content):
    return BeautifulSoup(content, 'html.parser')

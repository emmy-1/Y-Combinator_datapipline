import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    return response.text


def find_text(element,tag, class_name,default = None):
    found_text = element.find(tag, class_= class_name)
    return found_text.text if found_text else default

def find_html(element,tag, class_name,default = None):
    found_html = element.find(tag, class_= class_name)
    return found_html if found_html else default
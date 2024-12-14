from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import json
import re

imdb_url = 'https://www.imdb.com/'

parsed_actors_path = 'cache/parsed_actors.json' #<actor_url: set of movie_urls> from parsed actor pages
parsed_movies_path = 'cache/parsed_movies.json' #<movie_url: set of actor_urls> from parsed movie pages
actor_by_url_path = 'cache/actor_by_url.json'   #pairs of <url, actor_name>
movie_by_url_path = 'cache/movie_by_url.json'   #pairs of <url, movie_title>

actor_by_url = {}
movie_by_url = {}
parsed_actors = {}
parsed_movies = {}
costars = {}

driver = None

def save(url_dict: dict, path):
    with open(path, 'w') as f:
        json.dump(url_dict, f)

def load(path):
    with open(path, 'r') as f:
        cache = json.load(f)
    return cache

def load_cache():
    global actor_by_url, movie_by_url, parsed_actors,\
            parsed_movies, costars
    try:
        actor_by_url = load(actor_by_url_path)
        movie_by_url = load(movie_by_url_path)    
        parsed_actors = load(parsed_actors_path)
        parsed_movies = load(parsed_movies_path)
    except:
        print('[X] Failed to load cache')

def save_cache():
    try:
        save(actor_by_url, actor_by_url_path)
        save(movie_by_url, movie_by_url_path)
        save(parsed_movies, parsed_movies_path)
        save(parsed_actors, parsed_actors_path)
    except:
        print('[X] Failed to save cache')

def get_id(url):
    pattern = re.compile('(?:name|title)/([\w]*)/')
    return re.findall(pattern, url)[0]

def complete_url(url, opt="credits"):
    """returns url in format of 
    https://www.imdb.com/[name|title]/[actorid|titleid]/[option/]\n
    Keyword arguments:\n
    opt -- one of the values:\n
    'credits' -- option set to 'fullcredits'\n
    'summary' -- option set to 'plotsummary'\n
    None -- returns url with no option set
    """
    pattern = re.compile('((?:name|title)/[\w]*/)')
    link = re.findall(pattern, url)[0]
    link = urljoin(imdb_url, link)
    if opt is None:
        return link
    
    if opt == 'credits':
        link += 'fullcredits/'
    elif opt == 'summary':
        link += 'plotsummary/'

    return link
    
    

    
def driver_setup() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_prefs = {
        "intl.accept_languages": "en-US,en",
        "profile.default_content_setting_values": {"automatic_downloads": 1}
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)
    return driver

def actor_soup_by_url(actor_url: str):
    url = complete_url(actor_url)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def movie_soup_by_url(movie_url: str) -> BeautifulSoup:
    url = complete_url(movie_url)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def movie_description_by_url(movie_url):
    url = complete_url(movie_url, opt='summary')
    summary = ''
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        summary_div = soup.select('div[data-testid="sub-section-summaries"]')[0]
        summary_div = summary_div.find_all('li')
        summary = summary_div[0].text
    except Exception:
        print(f"No description for movie {url}")
    return summary


load_cache()
if __name__ == '__main__':
    pass 
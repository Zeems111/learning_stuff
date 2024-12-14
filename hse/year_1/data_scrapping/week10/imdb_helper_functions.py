from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def clean_url(url):
    pattern = re.compile('(\S*/[\w_/]*/)\?\S*')
    clean_url = str(re.findall(pattern, url)[0])
    return clean_url

def _driver_setup() -> webdriver.Chrome:
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

def actor_soup_by_url(actor_url: str) -> BeautifulSoup:
    driver = _driver_setup()
    driver.get(actor_url)
    
    max_scroll_attempts = 5
    scroll_attempts = 0
    clicks = 0
    gender = ('actor', 'actress')
    i = 0
    while scroll_attempts < max_scroll_attempts:
        expand_list_xpath = f'//*[@id="{gender[i]}-previous-projects"]/div[1]/label'
        try:
            expand_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, expand_list_xpath)))
            if clicks < 2:
                expand_button.click()
                clicks += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except(ElementClickInterceptedException, TimeoutException):
            i = 1 - i        
        scroll_attempts += 1
        #driver.execute_script("window.scrollTo(0, 0);")
        #time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
    if clicks < 2:
        print("Element not found after maximum scroll attempts")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")    
    
    driver.close()
    return soup

def movie_soup_by_url(movie_url: str) -> BeautifulSoup:
    driver = _driver_setup()
    driver.get(movie_url)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    return soup

if __name__ == '__main__':
    pass 
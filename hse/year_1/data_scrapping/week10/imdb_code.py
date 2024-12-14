from bs4 import BeautifulSoup
from imdb_helper_functions import clean_url, actor_soup_by_url
import urllib.parse

categories = set(['TV Series', 'TV Short', 'TV Episode', 
                     'TV Mini Series', 'TV Movie', 'TV Special', 
                     'Short', 'Video Game', 'Video', 
                     'Music Video', 'Podcast Series', 'Podcast Episode'])

imdb_url = 'https://www.imdb.com/'

def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    
    cast_table = cast_page_soup.find_all('table', {'class':'cast_list'})[0]
    cast_table = cast_table.find_all('td', {'class': None})

    cast = []
    for person in cast_table:
        t = person.find_all('a')[0]
        name = t.text.strip()
        url = clean_url(urllib.parse.urljoin(imdb_url, t.attrs['href']))
        cast.append((name, url))

    if num_of_actors_limit is not None and num_of_actors_limit < len(cast):
        cast = cast[:num_of_actors_limit]
    return cast


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    soup = actor_page_soup  
    movies = soup.find('div', {'id':'actor-previous-projects'})
    if movies is None:
        movies = soup.find('div', {'id':'actress-previous-projects'})

    movies = movies.find_all('div', 
                       {'class': 
                        'ipc-accordion__item__content_inner accordion-content'})[0]
    
    movies = movies.find_all('div', {'class': 'ipc-metadata-list-summary-item__tc'})
    
    feature_movies = []    
    for movie in movies:
        spans = movie.find_all('span', {'class': None})
        spans = set(span.text for span in spans)
        if not spans.intersection(categories):
            feature_movies.append(movie)

    feature_movies = [movie.find('a', {'class': 'ipc-metadata-list-summary-item__t'}) 
                        for movie in feature_movies]
    feature_movies = [(movie.text,
                       clean_url(
                            urllib.parse.urljoin(imdb_url, 
                                                movie.attrs['href'])) + 'fullcredits/')

                     for movie in feature_movies]
    
    if num_of_movies_limit is not None and num_of_movies_limit < len(feature_movies):
        feature_movies = feature_movies[:num_of_movies_limit]
    return feature_movies


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None):
    # your code here
    return # your code here


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here


if __name__ == '__main__':
    pass
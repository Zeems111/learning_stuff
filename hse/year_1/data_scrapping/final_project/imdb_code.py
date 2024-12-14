from bs4 import BeautifulSoup
import imdb_helper_functions as ihf
import math
import re



categories = set(['TV Series', 'TV Short', 'TV Episode', 
                     'TV Mini Series', 'TV Movie', 'TV Special', 
                     'Short', 'Video Game', 'Video', 
                     'Music Video', 'Podcast Series', 'Podcast Episode'])

imdb_url = 'https://www.imdb.com/'


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):  
    cast_table = cast_page_soup
    cast_table = cast_table.find_all('table', {'class':'cast_list'})[0]
    cast_table = cast_table.find_all('td', {'class': None})

    cast = []
    for person in cast_table:
        t = person.find_all('a')[0]
        name = t.text.strip()
        url = ihf.complete_url(t.attrs['href'])
        cast.append((name, url))

    if num_of_actors_limit is not None and num_of_actors_limit < len(cast):
        cast = cast[:num_of_actors_limit]
    return cast

def get_actors_by_movie_url(movie_url, num_of_actors_limit=None):
    movie_url = ihf.complete_url(movie_url)
    cast = ihf.parsed_movies.get(movie_url, None)

    if cast is None:
        cast = []
        print('Movie not in cache')
        cast_page_soup = ihf.movie_soup_by_url(movie_url)
        cast = get_actors_by_movie_soup(cast_page_soup)
        ihf.actor_by_url.update({url: name for name, url in cast})
        cast = [url for _, url in cast]
        ihf.parsed_movies[movie_url] = cast        

    if num_of_actors_limit is not None and num_of_actors_limit < len(cast):
        cast = cast[:num_of_actors_limit]
    
    return cast

def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):    
    soup = actor_page_soup
    soup = soup.find('div', id="filmography")
    pattern = re.compile('^(?:actor|actress)-*')
    divs = soup.find_all('div', id=pattern)
    all_movies = [div for div in divs if len(div.find_all('a')) == 1]

    feature_movies = []
    for movie in all_movies:
        feature = True
        for category in categories:    
            if category in movie.text:
                feature = False
                break
        if feature:
            feature_movies.append(movie)

    feature_movies = [movie.find('a') for movie in feature_movies]   
    feature_movies = [(movie.text,
                    ihf.complete_url(movie.attrs['href']))
                    for movie in feature_movies]    
    
    if num_of_movies_limit is not None and num_of_movies_limit < len(feature_movies):
        feature_movies = feature_movies[:num_of_movies_limit]
    return feature_movies 


def get_movies_by_actor_url(actor_url, num_of_movies_limit=None):
    actor_url = ihf.complete_url(actor_url)
    feature_movies = ihf.parsed_actors.get(actor_url, None)

    if feature_movies is None:
        feature_movies = []
        print('Actor not in cache')
        actor_page_soup = ihf.actor_soup_by_url(actor_url)
        feature_movies = get_movies_by_actor_soup(actor_page_soup)        
        ihf.movie_by_url.update({url: title for (title, url) in feature_movies})

        feature_movies = [url for _, url in feature_movies]
        ihf.parsed_actors[actor_url] = feature_movies        

    if num_of_movies_limit is not None and num_of_movies_limit < len(feature_movies):
        feature_movies = feature_movies[:num_of_movies_limit]
    return feature_movies 

def costars_by_actor(actor_url, num_of_actors_limit=None, 
                    num_of_movies_limit=None): 
    costars = []
    movies_to_check = get_movies_by_actor_url(actor_url, num_of_movies_limit)
    
    for movie in movies_to_check:
        actors = get_actors_by_movie_url(movie, num_of_actors_limit)
        costars.extend([x for x in actors if x not in costars])

    if actor_url in costars:
        costars.remove(actor_url)
    return costars

def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None,
        distance_limit=3):
    
    if actor_start_url == actor_end_url:
        return 0
    
    start = ihf.complete_url(actor_start_url)
    end = ihf.complete_url(actor_end_url)
    movie_distance = math.inf
    current_distance = 1
    actors_to_check = [start]
    next_wave_of_actors = []

    while current_distance <= distance_limit and movie_distance > current_distance:        
        current_actor = actors_to_check.pop()
        print(f'D{current_distance}: Checking {ihf.actor_by_url[current_actor]}: {current_actor}')
        
        costars = costars_by_actor(current_actor, 
                                   num_of_actors_limit=num_of_actors_limit, 
                                   num_of_movies_limit=num_of_movies_limit)
        
        print(f'Number of costars: {len(costars)}')
        if end in costars and movie_distance > current_distance:
            print(f'Set distance from {ihf.actor_by_url[start]} to '+
                    f'{ihf.actor_by_url[end]} at {current_distance}')
            movie_distance = current_distance
            break

        next_wave_of_actors.extend(costars)

        if not actors_to_check:
            actors_to_check.extend(next_wave_of_actors)
            next_wave_of_actors = []
            current_distance += 1   
    
    return movie_distance


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    movie_links = get_movies_by_actor_soup(actor_page_soup)
    movie_descriptions = []
    for movie_url in movie_links:
        description = ihf.movie_description_by_url(movie_url)
        movie_descriptions.append(description)

    return movie_descriptions


def get_movie_descriptions_by_actor_url(actor_url):
    actor_url = ihf.complete_url(actor_url)
    movie_links = ihf.parsed_actors.get(actor_url, None)

    if movie_links is None:
        actor_page_soup = ihf.actor_soup_by_url(actor_url)
        return get_movie_descriptions_by_actor_soup(actor_page_soup)         
    
    print(f'number of movies: {len(movie_links)}')
    movie_descriptions = []
    for movie_url in movie_links:
        description = ihf.movie_description_by_url(movie_url)        
        movie_descriptions.append(description)
        print(f'{len(movie_descriptions)}/{len(movie_links)}: {ihf.movie_by_url[movie_url]}')
    return movie_descriptions


if __name__ == '__main__':
    pass
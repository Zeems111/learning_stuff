def movie_discussability(movies, friends):
    discussability = {movie: 0 for movie in movies}
    for friend in friends:
        for movie in friend:
            discussability[movie] += 1
    return discussability


def dfs(graph, start_vertex, visited):
    stack = [start_vertex]
    visited.add(start_vertex)
    component = set()
    while stack:
        current_vertex = stack.pop()
        component.add(current_vertex)
        for adjacent in graph[current_vertex]:
            if adjacent not in visited:
                visited.add(adjacent)
                stack.append(adjacent)
    return component


def connected_components(graph):
    visited = set()
    components = [dfs(graph, vertex, visited) 
                  for vertex in graph 
                  if vertex not in visited]
    return components


def similar_movies(movies, similarities):
    graph = {movie: set() for movie in movies}
    for m1, m2 in similarities:
        graph[m1].add(m2)
        graph[m2].add(m1)
    
    groups = connected_components(graph)    
    similar_movies = {}
    for group in groups:
        for movie in group:
            similar_movies[movie] = group
    return similar_movies


def similar_movies_seen(movie, movie_group, discussability):
    movie_group.remove(movie)
    amount_seen_similar_movies = sum(discussability[film] 
                                     for film in movie_group)
    movie_group.add(movie)
    return amount_seen_similar_movies


def movie_uniqueness(movie, movie_group, discussability, num_of_friends):
    similar_movies_watched = similar_movies_seen(movie, 
                                                 movie_group, 
                                                 discussability)
    S = similar_movies_watched/num_of_friends        
    return 1/S if S else None


def calculate_score(movies, movie_groups, 
                    discussability, num_of_friends):
    best = ('No recommendation', 0)
    for movie in movies:
        _, best_score = best        
        group = movie_groups[movie]
        U = movie_uniqueness(movie, group, discussability, num_of_friends)
        if U is None:
            continue
        F = discussability[movie]
        score = F*U
        if best_score < score:
            best = movie, score        
    return best[0]


def recommend_movie(movies, similarities, friends):
    discussability = movie_discussability(movies, friends)
    groups = similar_movies(movies, similarities)
    number_of_friends = len(friends)
    best_movie = calculate_score(movies, groups, discussability, 
                                        number_of_friends)
    return best_movie


def check_input(movies, similarities, friends):
    if not similarities:
        raise ValueError("Empty input in similarities")
    if not friends:
        raise ValueError("Empty input in friends")
    temp = set()
    for item in similarities:
        temp.update(item)
    if temp.difference(movies):
        raise ValueError("Wrong movie in similarities")
    temp = set()
    for item in friends:
        temp.update(item)
    if temp.difference(movies):
        raise ValueError("Wrong movie in friends")
    return True 


if __name__ == '__main__':
    movies = ["Parasite","1917","Ford v Ferrari","Jojo Rabbit","Joker"]
    similarities = [["Parasite", "1917"],
                          ["Parasite", "Jojo Rabbit"],
                          ["Joker", "Ford v Ferrari"]]
    friends = [["Joker"],
                   ["Joker","1917"],
                   ["Joker"],
                   ["Parasite"],
                   ["1917"],
                   ["Jojo Rabbit", "Joker"]]

    movies = set(movies)
    correct_input = False
    try:
        correct_input = check_input(movies, similarities, friends)
    except Exception as e:
        print(e)
        print('No movie to recommend')
    
    if correct_input:
        best_recommendation = recommend_movie(movies, similarities, friends)
        print(f'Recommended movie: \"{best_recommendation}\"')

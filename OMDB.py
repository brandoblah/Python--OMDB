import json
import requests_with_caching

def get_movies_from_tastedive(moviename):
    response = requests_with_caching.get('https://tastedive.com/api/similar', params = {'q': moviename, 'type': 'movies', 'limit': 5}).json()
    return response

def extract_movie_titles(movie):
    extracted = []
    for i in movie['Similar']['Results']:
        extracted.append(i['Name'])
    return extracted

def get_related_titles(alist):
    if alist == []:
        return alist
    else:
        full = []
        for x in alist:
            i = extract_movie_titles(get_movies_from_tastedive(x))
            full.append(i)
        joined = full[0] + full[1]
        return list(set(joined))
    
def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    p = {'t': title, 'r': 'json'}
    response = requests_with_caching.get(baseurl, params = p)
    return response.json()
    
def get_movie_rating(movie):
    score = 0
    ratings = {}
    k = movie['Title']
    v = 0
    s_list = sorted(movie['Ratings'], key=lambda x: x['Value'])
    for i in range(len(s_list)):
        if s_list[i]['Source'] == "Rotten Tomatoes":
            score = s_list[i]['Value']
            if score != 0:
                str(score)
                v = score.strip("%")
            else:
                v = 0
    ratings[k] = v
    return int(ratings[k])
    

def movie_rating_by_title(movie):
    return get_movie_rating(get_movie_data(movie))

def get_sorted_recommendations(movietitles):
    #print(movietitles)
    movies = get_related_titles(movietitles)
    #print(movies)
    scores = [get_movie_rating(get_movie_data(movie)) for movie in movies]
    #print(scores)
    combo = zip(movies, scores)
    combo = sorted(combo, key=lambda x: (x[1], x[0]), reverse=True)
    #print(combo)
    movies = [movie for movie in combo]
    result = []
    for k, v in movies:
        result.append(k)
    return result
    
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
#get_movie_data("Bridesmaids")
print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))

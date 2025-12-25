import os
import time
import requests
import pandas as pd


API = os.getenv('API')
OMDBAPI = "http://www.omdbapi.com/"

#Функция для поиска шоу по заголовку и году
def tmdb_search(title, year):
    params = {"api_key": API, 
              "query": title, 
              "release_date.gte": f"{year}-01-01",
              "release_date.lte":f"{year}-12-31"
              } 
    response = requests.get(f"{OMDBAPI}/?apikey/movie", params=params)
    response.raise_for_status()
    return response.json().get('results', [])


def tmdb_details(t, id_):
    response = requests.get(f"{S}/{t}/{id_}", params={"api_key": API})
    response.raise_for_status()
    return response.json()





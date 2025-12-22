import os
import time
import requests
import pandas as pd


API = os.getenv('TMDB_KEY')
S = "http://www.omdbapi.com/"

def tmdb_search(title, year, typ):
    params = {"api_key": API, "query": title, "year": year} if typ == "Movie" else \
                            {"api_key":API, "query":title, "first_air_date_year":year}
    response = requests.get(f"{S}/search/{typ.lower()}", params=params)
    response.raise_for_status()
    return (response.json()["results"] or [None])[0]


def tmdb_details(t, id_):
    response = requests.get(f"{S}/{t}/{id_}", params={"api_key": API})
    response.raise_for_status()
    return response.json()





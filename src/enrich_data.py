import os
import time
from numpy import append
import requests
import pandas as pd


API = os.getenv('API')
OMDB_URL = "http://www.omdbapi.com/"

#Функция для поиска шоу по заголовку и году
def omdb_search(title, year):
    params = {"api_key": API, 
              "query": title, 
              "release_date.gte": f"{year}-01-01",
              "release_date.lte":f"{year}-12-31"
              } 
    response = requests.get(f"{OMDB_URL}/?apikey/movie", params=params)
    response.raise_for_status()
    return response.json().get('results', [])

#Функция для получения деталей шоу
def omdb_details(id_shows):
    response = requests.get(f"{OMDB_URL}/movie/{id_shows}", params={"api_key": API})
    response.raise_for_status()
    return response.json()


#Function data enrichment
def enrich_data_with_omdb(df):
    enriched_rows = []

    for _, row in df.iterrows():
        title = row['title']
        year = row['release_year']

        #Получаем результаты поиска
        search_results = omdb_search(title, year)
        if search_results:
            movie = search_results[0] #Берем первый результат
            details = omdb_details(movie['id']) # Получаем детали

            enriched_rows,append({
                "shows_id":row['show_id'],
                "omdb_id":movie['id'],
                "vote_average":details.get('vote_average'),
                "vote_count":details.get('vote_count'),
                "genres":', '.join(g['name'] for g in details.get('genres', [])),
                "runtime":details.get('runtime'),
                "release_date":details.get('runtime'),
                "overview":details.get('overview')
            })
        else:
            #Если нет результатов, просто добавим базовые даные
            enriched_rows.append({
                "shows_id":row['show_id'],
                "omdb_id":None,
                "vote_average":None,
                "vote_count":None,
                "genres":None,
                "runtime":None,
                "release_date":None,
                "overview":None
            })
        time.sleep(1) #Пауза меж запросами


#Пример использования 
df = pd.read_csv("data/processed/main.csv")
enriched_df = enrich_data_with_omdb(df)


#Save enrich data
enriched_df.to_csv("data/enriched/enriched_data.csv", index=False)




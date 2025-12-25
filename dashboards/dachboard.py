import pandas as pd
import streamlit as st
import plotly.express as px

# Загрузка данных
df = pd.read_csv("netflix_titles.csv")

# Очистка типов
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

st.title("Netflix Titles Dashboard")

# Фильтры
type_filter = st.sidebar.multiselect(
    "Тип контента",
    options=df['type'].dropna().unique(),
    default=df['type'].dropna().unique()
)

country_filter = st.sidebar.multiselect(
    "Страна",
    options=df['country'].dropna().unique(),
    default=None
)

year_min, year_max = int(df['release_year'].min()), int(df['release_year'].max())
year_range = st.sidebar.slider("Год выпуска", year_min, year_max, (year_min, year_max))

# Применение фильтров
filtered = df[df['type'].isin(type_filter)]
filtered = filtered[(filtered['release_year'] >= year_range[0]) & (filtered['release_year'] <= year_range[1])]
if country_filter:
    filtered = filtered[filtered['country'].isin(country_filter)]

# KPI
total_titles = len(filtered)
total_movies = len(filtered[filtered['type'] == "Movie"])
total_tvshows = len(filtered[filtered['type'] == "TV Show"])

col1, col2, col3 = st.columns(3)
col1.metric("Всего тайтлов", total_titles)
col2.metric("Фильмы", total_movies)
col3.metric("Сериалы", total_tvshows)

# График по годам
titles_by_year = filtered.groupby('release_year')['show_id'].count().reset_index()
fig_year = px.bar(titles_by_year, x='release_year', y='show_id', title="Тайтлы по годам")
st.plotly_chart(fig_year, use_container_width=True)

# Movies vs TV Shows
type_counts = filtered['type'].value_counts().reset_index()
type_counts.columns = ['type', 'count']
fig_type = px.pie(type_counts, names='type', values='count', title="Распределение по типу")
st.plotly_chart(fig_type, use_container_width=True)

# Топ стран
country_counts = (
    filtered['country']
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)
country_counts.columns = ['country', 'count']
fig_country = px.bar(country_counts, x='count', y='country', orientation='h', title="Топ-10 стран")
st.plotly_chart(fig_country, use_container_width=True)
from neo4j import GraphDatabase
from arango import ArangoClient
import streamlit as st
import time

# --------------------------
# NEO4J CONNECTION
# --------------------------
neo4j_driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "hello123")
)

def get_movies_by_genre(genre):
    query = """
    MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name: $genre})
    RETURN m.title AS title
    ORDER BY m.popularity DESC
    LIMIT 10
    """
    index_query = "CREATE INDEX genre_name_index IF NOT EXISTS FOR (g:Genre) ON (g.name)"
    time_before, time_after = measure_neo4j_query_time(query, {"genre": genre}, index_query)

    if "last_query_timings" not in st.session_state:
        st.session_state["last_query_timings"] = {}
    st.session_state["last_query_timings"]["Pencarian Genre"] = (time_before, time_after)

    with neo4j_driver.session() as session:
        result = session.run(query, genre=genre)
        return [record["title"] for record in result]


def search_movie_by_title(partial):
    query = """
    FOR m IN moviess
        FILTER CONTAINS(LOWER(m.title), LOWER(@title))
        SORT m.popularity DESC
        LIMIT 10
        RETURN m.title
    """
    index_query = None  # Tidak ada index yang bisa dibuat on-the-fly seperti Neo4j
    time_before, time_after = measure_arango_query_time(query, {"title": partial}, index_query)

    # Simpan hasil waktu ke session_state
    if "last_query_timings" not in st.session_state:
        st.session_state["last_query_timings"] = {}
    st.session_state["last_query_timings"]["Pencarian Judul"] = (time_before, time_after)

    cursor = adb.aql.execute(query, bind_vars={"title": partial})
    return list(cursor)


def get_cast_and_crew(title):
    query = """
    MATCH (m:Movie {title: $title})
    OPTIONAL MATCH (a:Actor)-[:ACTED_IN]->(m)
    OPTIONAL MATCH (d:Director)-[:DIRECTED]->(m)
    RETURN COLLECT(DISTINCT a.name) AS actors, COLLECT(DISTINCT d.name) AS directors
    """
    with neo4j_driver.session() as session:
        result = session.run(query, title=title)
        data = result.single()
        return data["actors"], data["directors"]

def get_all_genres():
    query = """
    MATCH (:Movie)-[:BELONGS_TO]->(g:Genre)
    RETURN DISTINCT g.name AS genre
    ORDER BY genre
    """
    with neo4j_driver.session() as session:
        result = session.run(query)
        genres = [record["genre"] for record in result if record["genre"]]
        return genres

# --------------------------
# ARANGODB CONNECTION
# --------------------------
client = ArangoClient()
adb = client.db("film_imdb", username="root", password="Binter366.")
movies_col = adb.collection("moviess")

def get_overview_for_title(title):
    query = """
    FOR m IN moviess
        FILTER m.title == @title
        RETURN { title: m.title, overview: m.overview }
    """
    def index_fn():
        movies_col.add_hash_index(fields=["title"], unique=False)

    time_before, time_after = measure_arango_query_time(query, {"title": title}, index_fn)

    # Simpan ke session_state
    if "last_query_timings" not in st.session_state:
        st.session_state["last_query_timings"] = {}
    st.session_state["last_query_timings"]["Overview Judul"] = (time_before, time_after)

    cursor = adb.aql.execute(query, bind_vars={"title": title})
    result = list(cursor)
    return result[0]["overview"] if result else "Overview tidak ditemukan"


def get_genre_and_rating_by_title(title):
    # --- Ambil genre dari Neo4j ---
    query = """
    MATCH (m:Movie {title: $title})
    OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
    RETURN collect(DISTINCT g.name) AS genres
    """
    with neo4j_driver.session() as session:
        result = session.run(query, title=title)
        record = result.single()
        genres = record["genres"] if record else []

    # --- Ambil rating dari ArangoDB ---
    rating_query = """
    FOR m IN moviess
        FILTER m.title == @title
        RETURN m.vote_average
    """
    cursor = adb.aql.execute(rating_query, bind_vars={"title": title})
    rating = list(cursor)
    rating_value = rating[0] if rating else None

    return genres, rating_value

def get_top_5_newest_movies():
    query = """
    FOR m IN moviess
        SORT m.release_date DESC
        LIMIT 5
        RETURN { title: m.title, overview: m.overview, release_date: m.release_date }
    """
    def create_index():
        adb.collection("moviess").add_hash_index(fields=["release_date"], unique=False)

    start_before = time()
    before_result = list(adb.aql.execute(query))
    end_before = time()

    create_index()

    start_after = time()
    after_result = list(adb.aql.execute(query))
    end_after = time()

    timing = (end_before - start_before, end_after - start_after)
    return after_result, timing


def get_top_5_popular_movies():
    query = """
    FOR m IN moviess
        SORT m.popularity DESC
        LIMIT 5
        RETURN { title: m.title, overview: m.overview, popularity: m.popularity }
    """
    return [doc for doc in adb.aql.execute(query)]

# --------------------------
# INDEXING + TIMING SUPPORT
# --------------------------

def measure_neo4j_query_time(query, params=None, index_query=None):
    with neo4j_driver.session() as session:
        start_before = time.time()
        session.run(query, **(params or {})).consume()
        end_before = time.time()
        time_before = end_before - start_before

        if index_query:
            session.run(index_query)

        start_after = time.time()
        session.run(query, **(params or {})).consume()
        end_after = time.time()
        time_after = end_after - start_after

    return time_before, time_after

def measure_arango_query_time(query, bind_vars=None, index_fn=None):
    start_before = time.time()
    list(adb.aql.execute(query, bind_vars=bind_vars or {}))
    end_before = time.time()
    time_before = end_before - start_before

    if index_fn:
        index_fn()

    start_after = time.time()
    list(adb.aql.execute(query, bind_vars=bind_vars or {}))
    end_after = time.time()
    time_after = end_after - start_after

    return time_before, time_after

def get_top_5_newest_movies_with_timing():
    query = """
    FOR m IN moviess
        SORT m.release_date DESC
        LIMIT 5
        RETURN { title: m.title, overview: m.overview, release_date: m.release_date }
    """
    def create_index():
        adb.collection("moviess").add_hash_index(fields=["release_date"], unique=False)
    
    before, after = measure_arango_query_time(query, index_fn=create_index)
    result = list(adb.aql.execute(query))
    return result, (before, after)

def get_top_5_popular_movies_with_timing():
    query = """
    FOR m IN moviess
        SORT m.popularity DESC
        LIMIT 5
        RETURN { title: m.title, overview: m.overview, popularity: m.popularity }
    """
    def create_index():
        adb.collection("moviess").add_hash_index(fields=["popularity"], unique=False)

    before, after = measure_arango_query_time(query, index_fn=create_index)
    result = list(adb.aql.execute(query))
    return result, (before, after)


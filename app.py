import streamlit as st
import random
from utils.queries import (
    search_movie_by_title,
    get_overview_for_title,
    get_cast_and_crew,
    get_genre_and_rating_by_title,
    get_movies_by_genre,
    get_all_genres,
    get_top_5_newest_movies_with_timing,
    get_top_5_popular_movies_with_timing
)
from textwrap import shorten

# 🎴 Daftar poster untuk di-random
posters = [
    r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\Blue and Purple Bold and Modern Best Friends Indie Movie Poster.png",
    r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\Sky Blue Lost Oasis Movie Poster.png",
    r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\Yellow Blue Bold Minimalist Documentary Movie Poster.png",
    r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\Beige Retro Style Movie Poster.png",
    r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\Black and Magenta TheatreBollywood Movie Poster.png"
]

def get_random_poster():
    return random.choice(posters)

def render_query_timings():
    current_page = st.session_state.get("page", "")
    if "last_query_timings" in st.session_state:
        relevant_keys = []

        if current_page == "Cari Judul":
            relevant_keys = ["Pencarian Judul", "Overview Judul"]
        elif current_page == "Pilih Genre":
            relevant_keys = ["Pencarian Genre"]
        elif current_page == "Beranda":
            relevant_keys = ["Top 5 Terbaru", "Top 5 Populer"]  # ⬅️ tambahkan ini

        display_timings = {k: v for k, v in st.session_state["last_query_timings"].items() if k in relevant_keys}

        if display_timings:
            st.markdown("---")
            st.markdown("## ⏱️ Perbandingan Waktu Eksekusi Query")
            for label, (before, after) in display_timings.items():
                st.markdown(f"- ⏰ **{label}**")
                st.markdown(f"  - Sebelum Indexing: `{before:.4f}` detik")
                st.markdown(f"  - Sesudah Indexing: `{after:.4f}` detik")

st.set_page_config(page_title="🎬 MoodieMovie", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
<style>
    /* Body / App Background */
    .stApp {
        background-color: #FCF7F1;
        color: #3E3E42;
        font-family: 'Poppins', sans-serif;
    }

    /* Header */
    header, [data-testid="stHeader"] {
        background-color: #FCF7F1;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #D7E3DC;
        color: #3E3E42;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #F2B5D4;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.2em;
        font-weight: 600;
        border: none;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #E493B3;
        color: white;
    }

    /* Headings */
    h1, h2, h3 {
        color: #3E3E42;
    }

    .stMarkdown h2 {
        color: #6D6875;
    }

    /* Input Fields */
    .stTextInput > div > input,
    .stMultiSelect > div > div {
        background-color: #fffefc;
        border-radius: 8px;
        padding: 0.4em;
        border: 1px solid #ddd;
    }

    /* Video Styling */
    video {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Misc spacing */
    .stMarkdown {
        font-size: 1.05em;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Beranda"

if "genre_redirect_to_judul" in st.session_state and st.session_state["genre_redirect_to_judul"]:
    st.session_state.page = "Cari Judul"
    st.session_state["genre_redirect_to_judul"] = False
    st.rerun()

with st.sidebar:
    st.markdown("# 🎬 MoodieMovie")
    page_options = ["Beranda", "Cari Judul", "Pilih Genre"]
    selected_page = st.radio("Pilih eksplorasi:", page_options, index=page_options.index(st.session_state.page), key="nav_menu")
st.session_state.page = selected_page

def highlight_genres(genres, selected_genres):
    highlighted = []
    for g in genres:
        if g in selected_genres:
            highlighted.append(f'<span style="color: white; background-color: #007bff; padding: 2px 6px; border-radius: 4px; font-weight: bold;">{g}</span>')
        else:
            highlighted.append(f'<span style="color: #333;">{g}</span>')
    return ', '.join(highlighted)

def render_beranda_detail(title):
    overview = get_overview_for_title(title)
    genres, rating = get_genre_and_rating_by_title(title)
    actors, directors = get_cast_and_crew(title)
    trailer = r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\Semester 6\\ROSBD\\DB\\DB\\855029-hd_1920_1080_30fps.mp4"

    st.markdown("---")
    st.markdown(f"### 🎬 {title}")

    if not overview:
        st.warning(f"Detail untuk '{title}' tidak ditemukan.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.video(trailer)
            except Exception as e:
                st.warning(f"⚠️ Gagal menampilkan trailer: {e}")

        st.markdown(f"**⭐ Rating:** {rating if rating else 'N/A'}")
        st.markdown(f"**🎭 Genre:** {', '.join(genres) if genres else 'Tidak tersedia'}")
        st.markdown(f"**📖 Sinopsis:** {overview}")
        st.markdown(f"**👥 Pemeran:** {', '.join(actors) if actors else 'Tidak tersedia'}")


        st.markdown("---")
        if st.button("❌ Tutup Detail", key=f"close_detail_{title}"):
            del st.session_state["selected_film"]
            del st.session_state["film_source_page"]
            st.rerun()

def render_simple_card(film, key_prefix, show_detail=False):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(get_random_poster(), width=120)
    with col2:
        st.markdown(f"**🎬 {film['title']}**")
        if 'release_date' in film:
            st.markdown(f"🗓️ {film['release_date']}")
        if 'popularity' in film:
            st.markdown(f"📈 Popularitas: {film['popularity']:.2f}")
        st.markdown(f"{film['overview'][:200]}...")
        if st.button("Tampilkan Detail", key=f"{key_prefix}_{film['title']}"):
            st.session_state["selected_film"] = film['title']
            st.session_state["film_source_page"] = "Beranda"

    if show_detail and st.session_state.get("selected_film") == film['title']:
        render_beranda_detail(film['title'])

def render_film_card(title, overview, rating, key, source_page="Cari Judul"):
    poster_path = get_random_poster()
    overview_snippet = shorten(overview, width=300, placeholder="...")
    col = st.columns([1, 3])
    with col[0]:
        st.image(poster_path, width=180)
    with col[1]:
        st.markdown(f"### 🎬 {title}")
        st.markdown(f"**📖 Ringkasan:** {overview_snippet}")
        st.markdown(f"**⭐ Rating:** {rating}")
        if st.button("Tampilkan Detail", key=key):
            st.session_state["selected_film"] = title
            st.session_state["film_source_page"] = source_page
            if source_page != "Beranda":
                st.session_state.page = source_page
            st.rerun()

if st.session_state.page == "Beranda":
    st.markdown("# 🎬 Selamat Datang di MOODIE MOVIE!")
    st.markdown("Temukan rekomendasi film terbaik sesuai seleramu. Gunakan kolom di sebelah kiri untuk mencari berdasarkan judul atau genre favoritmu..")
    st.markdown("Langsung scroll ke bawah dan jelajahi pilihan Film Terbaru dan Film Terpopuler yang lagi hits saat ini!")
    st.markdown("by sate avengers")

    st.markdown("---")
    st.subheader("📅 Film Terbaru")
    top5_newest, timing_new = get_top_5_newest_movies_with_timing()
    for film in top5_newest:
        render_simple_card(film, key_prefix="new", show_detail=True)

    st.subheader("🔥 Film Paling Populer")
    top5_popular, timing_pop = get_top_5_popular_movies_with_timing()
    for film in top5_popular:
        render_simple_card(film, key_prefix="pop", show_detail=True)

    # Simpan timing ke session state
    st.session_state["last_query_timings"] = {
        "Top 5 Terbaru": timing_new,
        "Top 5 Populer": timing_pop
    }


if st.session_state.page == "Cari Judul":
    st.subheader("🎬 Cari Film Berdasarkan Kata Kunci")
    selected_title = st.session_state.get("selected_film", None)
    source_page = st.session_state.get("film_source_page", "")
    if source_page != "Cari Judul":
        selected_title = None

    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("Masukkan kata kunci judul film")
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.pop("search_results", None)
            st.session_state.pop("selected_film", None)
            st.session_state.pop("last_query_timings", None)  # ⬅️ ini penting ditambahkan
            st.rerun()


    if not selected_title:
        if st.button("🔍 Cari"):
            result = search_movie_by_title(query)
            st.session_state["search_results"] = result or []
            st.rerun()

        if "search_results" in st.session_state and st.session_state["search_results"]:
            for idx, title in enumerate(st.session_state["search_results"]):
                overview = get_overview_for_title(title)
                _, rating = get_genre_and_rating_by_title(title)
                render_film_card(title, overview, rating, key=f"detail_{idx}")

    if selected_title:
        st.success(f"📌 **{selected_title}**")  
        overview = get_overview_for_title(selected_title)
        genres, rating = get_genre_and_rating_by_title(selected_title)
        actors, directors = get_cast_and_crew(selected_title)
        trailer = r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\\Semester 6\\ROSBD\\DB\\DB\\855029-hd_1920_1080_30fps.mp4"

        st.markdown(f"### 🎬 {selected_title}")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.video(trailer)

        st.markdown(f"**⭐ Rating:** {rating}")
        st.markdown(f"**🎭 Genre:** {', '.join(genres)}")
        st.markdown(f"**📖 Sinopsis:** {overview}")
        st.markdown(f"**👥 Pemeran:** {', '.join(actors)}")

        st.markdown("---")
        st.subheader("🎯 More Like This")
        all_movies = set()
        for genre in genres:
            related = get_movies_by_genre(genre)
            all_movies.update(related)

        recommended_movies = set()
        for movie in all_movies:
            if movie != selected_title:
                movie_genres, _ = get_genre_and_rating_by_title(movie)
                if set(genres).issubset(set(movie_genres)):
                    recommended_movies.add(movie)

        movie_list = sorted(recommended_movies)
        for i in range(0, len(movie_list), 3):
            cols = st.columns(3)
            for j, movie in enumerate(movie_list[i:i+3]):
                with cols[j]:
                    ov = get_overview_for_title(movie)
                    snippet = ov[:200] + "..." if len(ov) > 200 else ov
                    _, rat = get_genre_and_rating_by_title(movie)
                    st.image(get_random_poster(), width=140)
                    st.markdown(f"**🎬 {movie}**")
                    st.markdown(f"⭐ {rat}")
                    st.markdown(f"{snippet}")
                    if st.button(f"ℹ️ Detail: {movie}", key=f"more_judul_{movie}"):
                        st.session_state["selected_film"] = movie
                        st.session_state["film_source_page"] = "Cari Judul"
                        st.session_state.page = "Cari Judul"
                        st.rerun()


elif st.session_state.page == "Pilih Genre":
    # 🔄 Reset waktu pencarian judul agar tidak ditampilkan saat pilih genre
    if "last_query_timings" in st.session_state:
        st.session_state["last_query_timings"].pop("Pencarian Judul", None)

    st.subheader("🎭 Eksplorasi Berdasarkan Genre")

    genres_all = get_all_genres()
    genres_all = get_all_genres()
    col1, col2 = st.columns([4, 1])
    with col1:
        selected = st.multiselect("Pilih genre:", genres_all, default=st.session_state.get("last_genre_selected", []))
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.pop("last_genre_selected", None)
            st.session_state.pop("selected_film", None)
            st.session_state.pop("last_query_timings", None)
            st.rerun()

    if selected:
        st.session_state["last_genre_selected"] = selected

    mode = st.radio("🔎 Mode pencarian genre", ["Match Semua Genre", "Salah Satu Genre"], horizontal=True)
    selected_title = st.session_state.get("selected_film", None)
    source_page = st.session_state.get("film_source_page", "")
    if source_page != "Pilih Genre":
        selected_title = None

    if selected or selected_title:
        if mode == "Match Semua Genre":
            genre_sets = [set(get_movies_by_genre(g)) for g in selected]
            common_movies = set.intersection(*genre_sets) if genre_sets else set()
        else:
            genre_sets = [set(get_movies_by_genre(g)) for g in selected]
            common_movies = set.union(*genre_sets) if genre_sets else set()

        if selected_title:
            st.success(f"📌 **{selected_title}**")
            overview = get_overview_for_title(selected_title)
            genres, rating = get_genre_and_rating_by_title(selected_title)
            actors, directors = get_cast_and_crew(selected_title)
            trailer = r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\\Semester 6\\ROSBD\\DB\\DB\\855029-hd_1920_1080_30fps.mp4"

            st.markdown(f"### 🎬 {selected_title}")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.video(trailer)

            st.markdown(f"**⭐ Rating:** {rating}")
            st.markdown(f"**🎭 Genre:** {', '.join(genres)}")
            st.markdown(f"**📖 Sinopsis:** {overview}")
            st.markdown(f"**👥 Pemeran:** {', '.join(actors)}")

            st.markdown("---")
            if st.button("❌ Tutup Detail", key=f"close_detail_{selected_title}_genre"):
                del st.session_state["selected_film"]
                del st.session_state["film_source_page"]
                st.rerun()

            st.markdown("---")
            st.subheader("🎯 More Like This")
            all_movies = set()
            for genre in genres:
                related = get_movies_by_genre(genre)
                all_movies.update(related)

            recommended_movies = set()
            for movie in all_movies:
                if movie != selected_title:
                    movie_genres, _ = get_genre_and_rating_by_title(movie)
                    if mode == "Match Semua Genre":
                        if set(genres).issubset(set(movie_genres)):
                            recommended_movies.add(movie)
                    else:
                        if set(genres).intersection(set(movie_genres)):
                            recommended_movies.add(movie)

            movie_list = sorted(recommended_movies)
            for i in range(0, len(movie_list), 3):
                cols = st.columns(3)
                for j, movie in enumerate(movie_list[i:i+3]):
                    with cols[j]:
                        ov = get_overview_for_title(movie)
                        snippet = ov[:200] + "..." if len(ov) > 200 else ov
                        _, rat = get_genre_and_rating_by_title(movie)
                        st.image(get_random_poster(), width=140)
                        st.markdown(f"**🎬 {movie}**")
                        st.markdown(f"⭐ {rat}")
                        st.markdown(f"{snippet}")
                        if st.button(f"ℹ️ Detail: {movie}", key=f"more_{movie}"):
                            st.session_state["selected_film"] = movie
                            st.session_state["film_source_page"] = "Pilih Genre"
                            st.session_state.page = "Pilih Genre"
                            st.rerun()

        for m in sorted(common_movies):
            genres, rat = get_genre_and_rating_by_title(m)
            poster = get_random_poster()
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(poster, width=150)
            with col2:
                st.markdown(f"### 🎬 {m}")
                genre_html = highlight_genres(genres, selected)
                st.markdown(f"🎭 <b>Genre:</b> {genre_html}", unsafe_allow_html=True)
                if st.button(f"ℹ️ Info Selengkapnya: {m}", key=f"genre_info_{m}"):
                    st.session_state["selected_film"] = m
                    st.session_state["film_source_page"] = "Pilih Genre"
                    st.session_state.page = "Pilih Genre"
                    st.rerun()

if st.session_state.page in ["Beranda", "Cari Judul", "Pilih Genre"]:
    render_query_timings()


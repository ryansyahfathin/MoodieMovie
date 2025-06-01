# 🎬 MoodieMovie: Film Recommendation System with Neo4j + ArangoDB

MoodieMovie adalah sistem rekomendasi film yang dibangun menggunakan kombinasi **Graph Database (Neo4j)** dan **Document Database (ArangoDB)**. Sistem ini memungkinkan pengguna menemukan film berdasarkan **genre**, **judul**, dan **aktor**, serta melihat **overview** film yang relevan secara cepat dan efisien.

## 📂 Dataset

Kami menggunakan dataset **TMDB Movie Metadata (2024)** berisi 1 juta entri, yang digabungkan dengan **TMDB 5000 Movie Dataset**. Karena perbedaan fitur dan jumlah data, kami menambahkan atribut penting (seperti cast) dan melakukan **data synthesis** menggunakan Python `faker` untuk melengkapi kekurangan data. Dataset tersedia dalam format `.csv` dan diunduh dari Kaggle:

🔗 [TMDB Movie Metadata – Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

## 🗃️ Struktur Database

- **Neo4j (Graph DB)**: Menyimpan entitas `Movie`, `Genre`, `Actor`, dan relasi `BELONGS_TO`, `ACTED_IN`
- **ArangoDB (Document DB)**: Menyimpan metadata film lengkap dalam koleksi `moviess`  
  (field: `title`, `vote_average`, `release_date`, `runtime`, `homepage`, `overview`, `popularity`)

## 🎯 Tujuan

Sistem ini bertujuan:
- Menampilkan rekomendasi film berdasarkan **judul atau genre**
- Menyediakan overview film mirip dalam satu tampilan
- Menggabungkan kekuatan relasi entitas (graph) dan metadata film (dokumen)
- Mengoptimalkan pencarian menggunakan **indexing** pada dua jenis database

---

> Dengan MoodieMovie, pengguna bisa mengeksplor film tidak hanya dari genre yang disukai, tapi juga dari koneksi aktor & popularitasnya—semua tersaji dengan cepat dan rapi berkat integrasi dua database modern.


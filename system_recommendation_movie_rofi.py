# -*- coding: utf-8 -*-
"""System_Recommendation_Movie_Rofi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-ubLlJRoEmhvsDRy7tkn11q2d7hFHJjp

# **System_Recommendation: Movie Recommendation**

**Nama:** Muhammad Rofi'ul Arham

Project DBS Foundation x Dicoding

## Data Understanding

Dalam proyek ini, dataset yang digunakan adalah [Movie Recommendation](https://www.kaggle.com/datasets/rohan4050/movie-recommendation-data). Dataset ini terdiri dari 4 file CSV. Berikut adalah rincian dari dataset tersebut:

- Links: berisi daftar tautan eksternal untuk setiap film.
- Movies: berisi daftar film yang tersedia.
- Ratings: berisi penilaian pengguna terhadap film.
- Tags: berisi kata kunci atau label yang terkait dengan film.
"""

import pandas as pd

# Import semua file csv
links = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/sistem_rekomendasi/ml-latest-small/links.csv')
movies = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/sistem_rekomendasi/ml-latest-small/movies.csv')
ratings = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/sistem_rekomendasi/ml-latest-small/ratings.csv')
tags = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/sistem_rekomendasi/ml-latest-small/tags.csv')

# Menampilkan jumlah data setiap dataset
print('Jumlah data link movie : ', len(links.movieId.unique()))
print('Jumlah data movie : ', len(movies.movieId.unique()))
print('Jumlah data ratings dari user : ', len(ratings.userId.unique()))
print('Jumlah data ratings dari user : ', len(ratings.movieId.unique()))
print('Jumlah data : ', len(tags.movieId.unique()))

"""## Univariate Exploratory Data Analysis

Tahap penting untuk memahami kondisi awal data sebelum preprocessing.
Kita akan mengecek missing values, struktur data, dan kualitas data
pada setiap dataset untuk menentukan strategi pembersihan data.
"""

print("1. INFORMASI DATASET LINKS:")
print("Dataset links berisi ID eksternal untuk setiap film (IMDb, TMDb)")
print(links.info())

print("Missing values dalam dataset links:")
print(links.isnull().sum())

print("2. INFORMASI DATASET MOVIES:")
print("Dataset movies berisi judul film dan genre")
print(movies.info())

print("Missing values dalam dataset movies:")
print(movies.isnull().sum())

print("3. INFORMASI DATASET RATINGS:")
print("Dataset ratings berisi penilaian user terhadap film (1-5 skala)")
print(ratings.info())

print("Missing values dalam dataset ratings:")
print(ratings.isnull().sum())

print("Statistik deskriptif rating:")
print(ratings.describe())

print("4. INFORMASI DATASET TAGS:")
print("Dataset tags berisi kata kunci yang diberikan user untuk film")
print(tags.info())

print("Missing values dalam dataset tags:")
print(tags.isnull().sum())

"""Berdasarkan analisis di atas, ditemukan:
1. Dataset 'links' memiliki missing values pada kolom 'tmdbId' - perlu penanganan khusus
2. Dataset 'movies', 'ratings', dan 'tags' tidak memiliki missing values
4. Rating berdistribusi normal dengan rata-rata 3.5 dari skala 1-5

Terdapat missing values pada dataset links, tapi tidak akan mempengaruhi model karena kita tidak menggunakan tmdbId dalam sistem rekomendasi.

## Data Preprocessing

Pada tahap ini, kita akan menggabungkan dan membersihkan data dari berbagai  dataset untuk mempersiapkan data yang siap digunakan dalam modeling. Proses ini meliputi penggabungan dataset, penanganan missing values, dan standardisasi format data.
"""

import numpy as np

# Menggabungkan seluruh movieID pada kategori movie
movie_all = np.concatenate((
    links.movieId.unique(),
    movies.movieId.unique(),
    ratings.movieId.unique(),
    tags.movieId.unique(),
))

# Mengurutkan data dan menghapus data yang sama
movie_all = np.sort(np.unique(movie_all))

print('Jumlah seluruh data movie berdasarkan movieID: ', len(movie_all))

# Menggabungkan seluruh userId
user_all = np.concatenate((
    ratings.userId.unique(),
    tags.userId.unique(),

))

# Menghapus data yang sama kemudian mengurutkannya
user_all = np.sort(np.unique(user_all))

print('Jumlah seluruh user: ', len(user_all))

movie_info = pd.concat([links, movies, ratings, tags])
movie = pd.merge(ratings, movie_info , on='movieId', how='left')
movie

movie.isnull().sum()

movie.groupby('movieId').sum()

# Menggabungkan Data dengan Fitur Nama Movie

# Definisikan dataframe rating ke dalam variabel all_movie_rate
all_movie_rate = ratings
all_movie_rate

all_movie_name = pd.merge(all_movie_rate, movies[['movieId','title','genres']], on='movieId', how='left')
all_movie_name

# Menggabungkan dataframe genres dengan all_movie_name dan memasukkannya ke dalam variabel all_movie
all_movie = pd.merge(all_movie_name, tags[['movieId','tag']], on='movieId', how='left')
all_movie

"""## Data Preparation

Tahap persiapan data ini fokus pada pembersihan data final, penanganan
missing values, dan pembuatan struktur data yang optimal untuk kedua
model rekomendasi (Content-Based dan Collaborative Filtering).
"""

# Mengatasi missing value
all_movie.isnull().sum()

# Menghapus rows dengan missing values untuk memastikan kualitas data
all_movie_clean = all_movie.dropna()

print("Jumlah data setelah pembersihan:", len(all_movie_clean))

# Verifikasi kembali agar tidak ada missing values tersisa
print(all_movie_clean.isnull().sum())

# Mengurutkan data berdasarkan movieId
fix_movie = all_movie_clean.sort_values('movieId', ascending=True)

print('Jumlah film unik setelah pembersihan:', len(fix_movie.movieId.unique()))

# Menghapus duplikat untuk Content-Based Filtering
preparation = fix_movie.drop_duplicates('movieId')

print("Jumlah film unik untuk Content-Based:", len(preparation))

# Mengonversi data series ‘movieId’ menjadi dalam bentuk list
movie_id = preparation['movieId'].tolist()

# Mengonversi data series ‘title’ menjadi dalam bentuk list
movie_name = preparation['title'].tolist()

# Mengonversi data series ‘genres’ menjadi dalam bentuk list
movie_genre = preparation['genres'].tolist()

print(f"Jumlah film ID: {len(movie_id)}")
print(f"Jumlah nama film: {len(movie_name)}")
print(f"Jumlah genre film: {len(movie_genre)}")

# Membuat dictionary untuk data ‘movie_id’, ‘movie_name’, dan ‘movie_genre’
movie_data = pd.DataFrame({
    'id': movie_id,
    'movie_name': movie_name,
    'genre': movie_genre
})
movie_data

"""# Model Development dengan Content Based Filtering

Bagian ini mengembangkan model Content-Based Filtering menggunakan TF-IDF Vectorizer dan Cosine Similarity. Model ini merekomendasikan film berdasarkan kemiripan genre dengan film yang disukai user.

Content-Based Filtering merekomendasikan film berdasarkan kemiripan  karakteristik (genre) dengan film yang disukai user sebelumnya. Metode ini menggunakan TF-IDF untuk menganalisis genre dan Cosine Similarity untuk menghitung kemiripan antar film.
"""

# TF-IDF Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()

# Melakukan perhitungan idf pada data genre
tf.fit(movie_data['genre'])

# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names_out()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(movie_data['genre'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

# Membuat DataFrame untuk melihat matriks TF-IDF
# Kolom diisi dengan fitur (kata-kata) hasil ekstraksi dari TF-IDF
# Baris diisi dengan judul film

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names_out(),
    index=movie_data.movie_name
).sample(22, axis=1).sample(10, axis=0)

"""## Cosine Similarity"""

from sklearn.metrics.pairwise import cosine_similarity

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama resto
cosine_sim_df = pd.DataFrame(cosine_sim, index=movie_data['movie_name'], columns=movie_data['movie_name'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap resto
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""## Mendapatkan Rekomendasi

membuat fungsi movie_recommendations dengan beberapa parameter sebagai berikut:

- Nama_movie : Nama judul dari movie (index kemiripan dataframe).
- Similarity_data : Dataframe mengenai similarity yang telah kita didefinisikan sebelumnya
- Items : Nama dan fitur yang digunakan untuk mendefinisikan kemiripan, dalam hal ini adalah ‘movie_name’ dan ‘genre’.
- k : Banyak rekomendasi yang ingin diberikan.
"""

def movie_recommendations(nama_movie, similarity_data=cosine_sim_df, items=movie_data[['movie_name', 'genre']], k=5):


    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_movie].to_numpy().argpartition(
        range(-1, -k, -1))

    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop nama_movie agar nama movie yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_movie, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

movie_data[movie_data.movie_name.eq('John Wick (2014)')]

"""dari hasil di atas dapat dilihat bahwa pengguna menyukai movie yang berjudul John Wick (2014) yang bergenre Action dan Thriller.
Kemudian kita coba untuk mendapatkan rekomendasi movie yang mirip dengan John Wick (2014).
"""

# Mendapatkan rekomendasi film (movie) yang mirip dengan John Wick (2014)
movie_recommendations('John Wick (2014)')

"""## Evaluation

Evaluasi kuantitatif untuk Content-Based Filtering menggunakan Precision@K dan evaluasi kualitas rekomendasi berdasarkan relevansi genre. Evaluasi ini penting untuk mengukur performa model.
"""

def evaluate_content_based_precision(test_movies, k=5, similarity_threshold=0.1):
    """
    Menghitung Precision@K untuk Content-Based Filtering

    Parameters:
    - test_movies: List film untuk ditest
    - k: Jumlah rekomendasi (K)
    - similarity_threshold: Threshold minimum untuk dianggap relevan

    Returns:
    - Average Precision@K
    """
    precisions = []

    for movie in test_movies:
        if movie in cosine_sim_df.index:
            # Dapatkan rekomendasi
            recommendations = movie_recommendations(movie, k=k)

            if len(recommendations) > 0:
                # Hitung relevansi berdasarkan genre similarity
                original_genre = movie_data[movie_data.movie_name == movie]['genre'].iloc[0]
                original_genres = set(original_genre.lower().split('|'))

                relevant_count = 0
                for _, rec_movie in recommendations.iterrows():
                    rec_genres = set(rec_movie['genre'].lower().split('|'))
                    # Hitung intersection genre
                    common_genres = len(original_genres.intersection(rec_genres))
                    total_genres = len(original_genres.union(rec_genres))

                    # Relevan jika ada overlap genre yang signifikan
                    if common_genres / total_genres >= similarity_threshold:
                        relevant_count += 1

                precision = relevant_count / k
                precisions.append(precision)

    return np.mean(precisions) if precisions else 0

# Test dengan sample film dari berbagai genre
print("\n=== EVALUASI PRECISION@K ===")
print("Menguji Precision@5 dengan sample film dari berbagai genre...")

test_movies_sample = [
    'John Wick (2014)',
    'Toy Story (1995)',
    'Forrest Gump (1994)',
    'The Matrix (1999)',
    'Titanic (1997)'
]

# Filter film yang ada dalam dataset
available_test_movies = [movie for movie in test_movies_sample if movie in movie_data.movie_name.values]
print(f"Film test yang tersedia: {len(available_test_movies)} dari {len(test_movies_sample)}")

if available_test_movies:
    precision_at_5 = evaluate_content_based_precision(available_test_movies, k=5, similarity_threshold=0.2)

    print(f"\n=== HASIL EVALUASI CONTENT-BASED FILTERING ===")
    print(f"Precision@5: {precision_at_5:.4f}")
    print(f"Persentase: {precision_at_5*100:.2f}%")

    print(f"\nInterpretasi:")
    if precision_at_5 >= 0.8:
        print("Excellent: Model memberikan rekomendasi yang sangat relevan")
    elif precision_at_5 >= 0.6:
        print("Good: Model memberikan rekomendasi yang cukup relevan")
    elif precision_at_5 >= 0.4:
        print("Fair: Model memberikan rekomendasi dengan relevansi sedang")
    else:
        print("Poor: Model perlu improvement untuk meningkatkan relevansi")

    print(f"\nMetrik Precision@K mengukur proporsi rekomendasi yang relevan")
    print(f"dari total K rekomendasi yang diberikan. Nilai 1.0 berarti semua")
    print(f"rekomendasi relevan, sedangkan 0.0 berarti tidak ada yang relevan.")

"""# Model Development dengan Collaborative Filtering

## Data Understanding
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt

df = ratings
df

"""## Data Preparation"""

# Mengubah userID menjadi list tanpa nilai yang sama
user_ids = df['userId'].unique().tolist()
print('list userID: ', user_ids)

# Melakukan encoding userID
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded userID : ', user_to_user_encoded)

# Melakukan proses encoding angka ke ke userID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke userID: ', user_encoded_to_user)

# Mengubah movieId menjadi list tanpa nilai yang sama
movie_ids = df['movieId'].unique().tolist()

# Melakukan proses encoding movieId
movie_to_movie_encoded = {x: i for i, x in enumerate(movie_ids)}

# Melakukan proses encoding angka ke movieId
movie_encoded_to_movie = {i: x for i, x in enumerate(movie_ids)}

# Mapping userId ke dataframe genres
df['genres'] = df['userId'].map(user_to_user_encoded)

# Mapping movieD ke dataframe movies
df['movies'] = df['movieId'].map(movie_to_movie_encoded)

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)

# Mendapatkan jumlah movie
num_movie = len(movie_encoded_to_movie)
print(num_movie)

# Mengubah rating menjadi nilai float
df['ratings'] = df['rating'].values.astype(np.float32)

# Nilai minimun rating
min_rating = min(df['rating'])

# Nilai maksimal rating
max_rating = max(df['rating'])

print('Number of User: {}, Number of movie: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_movie, min_rating, max_rating
))

"""## Membagi Data untuk Training dan Validasi"""

# Mengacak data untuk menghindari bias
df = df.sample(frac=1, random_state=42)
df

# Membuat variabel x untuk mencocokkan data genres  dan movies menjadi satu value
x = df[['genres', 'movies']].values

# Membuat variabel y untuk membuat ratings dari hasil
y = df['ratings'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

print(x, y)

"""## Proses Training

Membuat model Neural Network untuk Collaborative Filtering. Menggunakan embedding layers untuk user dan movie, serta bias terms untuk memprediksi rating yang akan diberikan user pada suatu film.
"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_movie, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_movie = num_movie
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.movie_embedding = layers.Embedding( # layer embeddings movies
        num_movie,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.movie_bias = layers.Embedding(num_movie, 1) # layer embedding movies bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    movie_vector = self.movie_embedding(inputs[:, 1]) # memanggil layer embedding 3
    movie_bias = self.movie_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)

    x = dot_user_movie + user_bias + movie_bias

    return tf.nn.sigmoid(x) # activation sigmoid

model = RecommenderNet(num_users, num_movie, 50) # inisialisasi model

# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

# Memulai training
history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 20,
    validation_data = (x_val, y_val)
)

"""## Visualisasi Metrik

Visualisasi metrik training untuk menganalisis performa model
selama proses training. Grafik menunjukkan tren RMSE pada
training dan validation set.
"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""## Mendapatkan rekomendasi film (movie)"""

# Menyalin data movie_data ke dalam variabel movie_df
movie_df = movie_data

# Membaca file ratings.csv yang berisi data rating pengguna terhadap film
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/sistem_rekomendasi/ml-latest-small/ratings.csv')

# Mengambil secara acak satu userId dari data rating
user_id = df.userId.sample(1).iloc[0]

# Mengambil semua film yang telah ditonton oleh user tersebut
movie_watched_by_user = df[df.userId == user_id]

# Menentukan daftar ID film yang belum ditonton oleh user tersebut
movie_not_watched = movie_df[~movie_df['id'].isin(movie_watched_by_user.movieId.values)]['id']

# Menyaring hanya film yang ada dalam dictionary movie_to_movie_encoded
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)

# Mengubah ID film yang belum ditonton ke bentuk encoded (numerik)
movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]

# Mengubah user ID menjadi bentuk encoded (numerik)
user_encoder = user_to_user_encoded.get(user_id)

# Membuat array gabungan berisi pasangan (user_encoded, movie_encoded)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

# Memprediksi rating yang mungkin diberikan user terhadap film yang belum ditonton
ratings = model.predict(user_movie_array).flatten()

# Mengambil indeks dari 10 prediksi rating tertinggi
top_ratings_indices = ratings.argsort()[-10:][::-1]

# Mengubah indeks encoded film ke ID film asli berdasarkan prediksi terbaik
recommended_movie_ids = [
    movie_encoded_to_movie.get(movie_not_watched[x][0]) for x in top_ratings_indices
]

# Menampilkan rekomendasi untuk user tertentu
print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)

# Menampilkan film dengan rating tertinggi yang sudah pernah ditonton user
print('movie with high ratings from user')
print('----' * 8)

# Mengambil 5 film dengan rating tertinggi yang pernah ditonton user tersebut
top_movie_user = (
    movie_watched_by_user.sort_values(
        by='rating',
        ascending=False
    )
    .head(5)
    .movieId.values
)

# Menampilkan nama dan genre dari 5 film favorit user
movie_df_rows = movie_df[movie_df['id'].isin(top_movie_user)]
for row in movie_df_rows.itertuples():
    print(row.movie_name, ':', row.genre)

print('----' * 8)

# Menampilkan 10 rekomendasi film berdasarkan hasil prediksi model
print('Top 10 movie recommendation')
print('----' * 8)

recommended_movie = movie_df[movie_df['id'].isin(recommended_movie_ids)]
for row in recommended_movie.itertuples():
    print(row.movie_name, ':', row.genre)


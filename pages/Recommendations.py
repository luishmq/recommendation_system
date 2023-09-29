import pandas as pd
import numpy as np
import streamlit as st
from scipy.sparse import csr_matrix
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from PIL                  import Image

def load_data():
    df_ratings = pd.read_csv('data/Ratings.csv', nrows=50000, low_memory=False)
    df_books = pd.read_csv('data/Books.csv', low_memory=False)
    
    return df_ratings, df_books

def drop_columns(df_books, df_ratings):
    df_books = df_books.drop( columns=['Image-URL-M', 'Image-URL-S', 'Year-Of-Publication', 'Publisher',
                                        'Book-Author'], axis=1 )


    df_books.columns = ['isbn', 'book_title', 'image_url_l']
    df_ratings.columns = ['user_id', 'isbn', 'book_rating']
    return df_books, df_ratings

def data_preparation(df_books, df_ratings):
    df_books = df_books.dropna(subset='image_url_l')

    df1 = pd.merge(df_ratings, df_books, on='isbn')

    df_counts = df1['user_id'].value_counts().reset_index()

    df_counts.columns = ['user_id', 'counts']

    df2 = pd.merge(df1, df_counts, on='user_id')

    df2_filtered = df2[df2['counts'] > 999]

    df2_filtered = df2_filtered.copy()

    df2_filtered.drop_duplicates(['user_id','book_title'], inplace = True)

    return df2_filtered

def pivot(df2_filtered):
    books_pivot = df2_filtered.pivot_table(columns = 'user_id', index = 'book_title', values = 'book_rating')

    books_pivot.fillna(0, inplace = True)

    return books_pivot

def scores(books_pivot):
    books_sparse = csr_matrix(books_pivot)

    similarity_scores = cosine_similarity(books_sparse)

    return similarity_scores

def recommend(book_name, df2_filtered):
    # index fetch
    index = np.where(books_pivot.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    recommended_books = []

    for i in similar_items:
        recommended_book_name = books_pivot.index[i[0]]
        recommended_book_data = df2_filtered[df2_filtered['book_title'] == recommended_book_name].iloc[0]
        recommended_books.append((recommended_book_name, recommended_book_data['image_url_l']))

    return recommended_books

# Carregar os dados e criar as estruturas necessárias

df_ratings, df_books = load_data()
df_books, df_ratings = drop_columns(df_books, df_ratings)
df2_filtered = data_preparation(df_books, df_ratings)
books_pivot = pivot(df2_filtered)
similarity_scores = scores(books_pivot)

# Configuração da página Streamlit

st.set_page_config(layout='wide')
st.title("Sistema de Recomendação de Livros 💡")

image = Image.open('imgs/system_img.png') 
st.sidebar.image(image)

# Interface de entrada do usuário
user_input = st.text_input("Digite o nome do livro desejado:")

if user_input:
    # Verificar se o livro está na base de dados
    if user_input in books_pivot.index:
        recommendations_with_images = recommend(user_input, df2_filtered)

        st.header("Livros Recomendados:")
        for i, (recommended_book_name, recommended_book_image_url) in enumerate(recommendations_with_images):
            st.write(f"Sugestão {i + 1}: {recommended_book_name}")
            st.image(recommended_book_image_url, width=100, caption=recommended_book_name)
    else:
        st.warning("O livro inserido não foi encontrado na base de dados.")

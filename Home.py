import streamlit as st
from PIL                  import Image

st.set_page_config(
    page_title="Sistema de Recomendação de Livros",
    page_icon="📚",
    layout='wide'
)

st.title("Bem-vindo(a) ao painel do Projeto de Sistema de Recomendação de Livros! 📚")

image = Image.open('imgs/google.png') 
st.sidebar.image(image)

st.markdown(
    """
     #### O que é um Sistema de Recomendação 💡?

     Um sistema de recomendação é uma classe de aplicativos de software e técnicas que fornecem sugestões ou recomendações personalizadas aos usuários. Essas recomendações podem ser sobre uma variedade de itens, como produtos, serviços, conteúdo digital (filmes, músicas, artigos), amigos ou qualquer outra coisa que possa ser recomendada com base nos interesses e preferências dos usuários. A principal finalidade de um sistema de recomendação é ajudar os usuários a encontrar itens relevantes e interessantes em meio a uma vasta quantidade de opções disponíveis.

     ##### No caso dessa aplicação, o objetivo é encontrar sugestões de livros a partir de um dado livro escolhido inicial.

    """
)
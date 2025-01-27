import streamlit as st

def render(data, filtros):
    st.title("Atividade Extra")
    st.write("Filtros aplicados:", filtros)
    st.write(data.head())  # Exemplo simples de exibição


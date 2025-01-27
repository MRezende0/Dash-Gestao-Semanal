import streamlit as st

def render(data, filtros):
    st.title("Auditoria")
    st.write("Filtros aplicados:", filtros)
    st.write(data.head())
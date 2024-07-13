import streamlit as st
from cg.data_container import DataContainer


@st.cache_resource
def load_data():
    return DataContainer.init('data/go')


data = load_data()

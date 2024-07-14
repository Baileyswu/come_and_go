import streamlit as st
from cg.manager import Manager
from cg.data_container import DataContainer
from cg.plotter import Plotter


@st.cache_resource
def load_data():
    return DataContainer.init('data/go')


@st.cache_resource
def init_manager():
    return Manager(data)


@st.cache_resource
def init_plotter():
    return Plotter(data)


data = load_data()
mg = init_manager()
plotter = init_plotter()

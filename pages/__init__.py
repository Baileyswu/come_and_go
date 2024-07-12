import streamlit as st
from cg.manager import Manager


@st.cache_resource
def init_manager():
    return Manager.decide_sub('data/go')


mg = init_manager()

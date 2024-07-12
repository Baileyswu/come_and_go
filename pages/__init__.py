import streamlit as st
from cg.manager import Manager


@st.cache_resource
def init_manager():
    return Manager('data/go').decide_sub()

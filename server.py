from pages import label, plot
from cg.log import logger
import streamlit as st


def next_page():
    if 'page' not in st.session_state:
        st.session_state.page = 'label'

    if st.session_state.page == 'label':
        label.run()
    elif st.session_state.page == 'plot':
        plot.run()

    if st.button('Next'):
        if st.session_state.page == 'label':
            st.session_state.page = 'plot'
        else:
            st.session_state.page = 'label'


if __name__ == '__main__':
    pass

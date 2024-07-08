import streamlit as st
from cg.plotter import Plotter

@st.cache_resource
def init_plotter():
    return Plotter('data/go')

plotter = init_plotter()


def run():
    if st.button('重载数据'):
        plotter.reload_file()
    data, x, y = plotter.month_stats(2024)
    st.bar_chart(data,x=x, y=y)


if __name__ == '__main__':
    run()
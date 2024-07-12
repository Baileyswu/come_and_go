import streamlit as st
from cg.echarts import bar_stack
from cg.plotter import Plotter
from pages import mg


@st.cache_resource
def init_plotter():
    return Plotter(mg)


plotter = init_plotter()


def run():

    data, x, y, hue = plotter.month_stats(2024, '支出')
    bar_stack(data, x, y, hue)

    cats = data['分类'].drop_duplicates().tolist()
    for cat in cats:
        data, x, y, hue = plotter.month_sub_stats(2024, cat)
        bar_stack(data, x, y, hue)

    data, x, y, hue = plotter.month_stats(2024, '收入')
    bar_stack(data, x, y, hue)


if __name__ == '__main__':
    run()

import streamlit as st
from cg.echarts import bar_stack
from pages import plotter


def run():
    plotter.month_stats(2024, '支出')
    plotter.month_stats(2024, '收入')


if __name__ == '__main__':
    run()

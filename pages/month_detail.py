import streamlit as st
from cg.log import logger
from cg.echarts import bar_stack, pie
from pages import plotter, data


def run():
    lc, rc = st.columns([1, 1])
    # with lc:
    cols = st.columns(4)
    year = cols[0].selectbox('选择年份', data.get_years())
    month = cols[1].selectbox('选择月份', data.get_months(year))
    logger.info(data.get_label_set())
    cat = cols[2].selectbox('选择类别', data.get_cat_set())
    logger.info(cat)
    st.write(year, month, cat)
    df = plotter.month_detail(year, month, cat)

    # with rc:
    st.write('total', df['金额'].sum().round(2))
    st.data_editor(df)


if __name__ == '__main__':
    run()

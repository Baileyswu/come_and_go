import streamlit as st
import pandas as pd
from cg.manager import Manager
from cg import logger


ENTRY = {
    0: '支出',
    1: '收入'
}

@st.cache_resource
def init_manager():
    m = Manager('data/dirty.csv', 'data/clean.csv')
    return m


def show_selected():
    df = m.select_ones()
    st.write(df)
    return df


def show_options():
    label_set = m.get_label_set()
    cols = st.columns(2)
    options = [
        cols[i].selectbox(ENTRY[i], [label for label in label_set if label.startswith(ENTRY[i])])
        for i in range(2)
    ]
    return options


def operate(options, df):
    cols = st.columns(2)
    for i in range(2):
        if cols[i].button(f'确认{ENTRY[i]}'):
            df = m.get_label_and_move(df, options[i])
            st.write(df)
            st.write('还需打标:', m.get_dirty_size())
            st.write('已经存储数据:', m.get_clean_size())
            st.write('位置:', m.clean_path)
    # sp = m.sweep()
    # st.write(sp)


if __name__ == '__main__':
    logger.info('-------------------- streamlit app ----------------------')
    m = init_manager()
    if m.get_dirty_size() > 0:
        df = show_selected()
        options = show_options()
        logger.info(options)
        operate(options, df)
    else:
        st.write('打标完成！')
    logger.info('end server')
import streamlit as st
import pandas as pd
from cg.manager import Manager
from cg.log import logger

ENTRY = {
    0: '支出',
    1: '收入'
}

@st.cache_resource
def init_manager():
    return Manager('data/dirty.csv', 'data/clean.csv')

mg = init_manager()


def show_selected():
    df = mg.get_head()
    st.write(df)
    return df


def show_options():
    label_set = mg.get_label_set()
    cols = st.columns(2)
    options = [
        cols[i].selectbox(ENTRY[i], [label for label in label_set if label.startswith(ENTRY[i])])
        for i in range(2)
    ]
    return options


def operate(col, option, df, entry):
    if col.button(f'确认{entry}'):
        df = mg.get_label_and_move(df, option)
        st.write('打标结果', '（还需打标:', mg.get_dirty_size(), ', 已经存储:', mg.get_clean_size(), '）')
        st.write(df)
        st.write('位置:', mg.clean_path)
    # sp = mg.sweep()
    # st.write(sp)


def show_operations(options, df):
    cols = st.columns(2)
    for i in range(2):
        operate(cols[i], options[i], df, ENTRY[i])


def show_refresh():
    if st.button('下一条'):
        mg.update_head()


def whole_page():
    if mg.get_dirty_size() > 0:
        show_refresh()
        df = show_selected()
        options = show_options()
        logger.info(options)
        show_operations(options, df)
    else:
        st.write('打标完成！')

def run():
    logger.info('-------------------- labeling ----------------------')
    whole_page()
    logger.info('end label')
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
    m = Manager('data/dirty.csv', 'data/clean.csv')
    return m


def show_selected():
    if st.button('下一条'):
        m.update_head()
    df = m.get_head()
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


def operate(col, option, df, entry):
    if col.button(f'确认{entry}'):
        df = m.get_label_and_move(df, option)
        st.write('打标结果', '（还需打标:', m.get_dirty_size(), ', 已经存储:', m.get_clean_size(), '）')
        st.write(df)
        st.write('位置:', m.clean_path)
    # sp = m.sweep()
    # st.write(sp)


def show_operations(options, df):
    cols = st.columns(2)
    for i in range(2):
        operate(cols[i], options[i], df, ENTRY[i])


if __name__ == '__main__':
    logger.info('-------------------- streamlit app ----------------------')
    m = init_manager()
    if m.get_dirty_size() > 0:
        df = show_selected()
        options = show_options()
        logger.info(options)
        show_operations(options, df)
    else:
        st.write('打标完成！')
    logger.info('end server')
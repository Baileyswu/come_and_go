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
    return Manager('data/go')

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
        st.write(df)
        sp = mg.sweep()
        if sp is not None and len(sp) > 0:
            st.write('同类整理')
            st.write(sp)


def show_operations(options, df):
    cols = st.columns(2)
    for i in range(2):
        operate(cols[i], options[i], df, ENTRY[i])


def show_refresh(con):
    if con.button('刷新'):
        mg.update_head()


def show_skip(con):
    if con.button('跳过'):
        mg.skip_label(mg.get_head())
        mg.update_head()


def show_left(con):
    con.write(f'还需打标:{mg.get_dirty_size()}')


def whole_page():
    if mg.get_dirty_size() > 0:
        c = st.columns(3)
        show_refresh(c[0])
        show_skip(c[1])
        show_left(c[2])
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


if __name__ == '__main__':
    run()
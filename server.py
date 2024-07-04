import streamlit as st
import pandas as pd
from cg.manager import Manager


if __name__ == '__main__':
    m = Manager('data/dirty.csv', 'data/clean.csv')
    if m.get_dirty_size() > 0:
        df = m.select_ones()
        st.write(df)
        st.write('还需打标:', m.get_dirty_size())
        st.write('已经存储数据:', m.get_clean_size(), '位置:', m.clean_path)

        option = st.selectbox('打标', m.label_set)
        if st.button('确认'):
            df = m.get_label_and_move(df, option)
            st.write(df)
            # sp = m.sweep()
            # st.write(sp)
    else:
        st.write('打标完成！')
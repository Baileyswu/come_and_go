import streamlit as st
from cg.log import logger
from cg.echarts import bar_stack, pie
from pages import plotter, data, mg


def run():
    with st.container(border=True):
        cols = st.columns(4)
        year = cols[0].selectbox('选择年份', data.get_years(),
                                 index=st.session_state.get('year'))
        month = cols[1].selectbox('选择月份', data.get_months(year),
                                  index=st.session_state.get('month'))
        cat = cols[2].selectbox('选择类别', data.get_cat_set(),
                                index=st.session_state.get('cat'))
        if year is not None:
            st.session_state['year'] = data.get_years().index(year)
        if month is not None:
            st.session_state['month'] = data.get_months(year).index(month)
        if cat is not None:
            st.session_state['cat'] = data.get_cat_set().index(cat)
        logger.info(cat)
        st.write(year, month, cat)
        df = plotter.month_detail(year, month, cat)

    with st.container(border=True):
        edit_key = 'online_edit'
        # if st.session_state.get(edit_key) is None:
        #     st.session_state[edit_key] = {}
        st.write('sum', df['金额'].sum().round(2))
        show_columns = ['备注', '交易时间', '金额', 'label']
        edited = st.data_editor(
            df[show_columns],
            key=edit_key,
            num_rows='dynamic',
            column_config={
                # '交易时间': st.column_config.DateColumn('交易时间', format='YYYY-MM-DD'),
                'label': st.column_config.SelectboxColumn('label', options=data.get_label_set()),
            },
            hide_index=True,
        )
        st.write(st.session_state.get(edit_key))
        if st.button('保存'):
            st.write('total', len(edited))
            mg.update_clean(st.session_state.get(edit_key), df.index.tolist())
            logger.info(f'clean session_state.{edit_key}')
            st.session_state[edit_key].update({'added_rows': []})
            st.session_state[edit_key].update({'edited_rows': {}})
            st.session_state[edit_key].update({'deleted_rows': []})


if __name__ == '__main__':
    run()

import logging
from cg.manager import Manager
from cg.data_container import DataContainer


def test_manager_head():
    data = DataContainer.init('data/go')
    m = Manager(data)
    logging.info(f'manager head \n{m.head}')
    df = m.get_head()
    df = m.get_head()
    m.update_head()
    df = m.get_head()


def test_manager_label():
    data = DataContainer.init('data/go')
    m = Manager(data)
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')


def test_manager_sweep():
    data = DataContainer.init('data/go')
    m = Manager(data)
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
    m.sweep()


def test_manager_skip():
    data = DataContainer.init('data/go')
    m = Manager(data)
    df = m.get_head()
    m.skip_label(df)


def test_manager_update():
    import pandas as pd
    data = DataContainer.init('data/go')
    m = Manager(data)
    df = pd.DataFrame({
        '交易时间': ['2024-07-16'],
        '金额': [100.55],
        'label': ['支出-交通-燃料/充电'],
    })
    start_id = data.clean.index.max() + 1
    df = df.set_index(pd.Index(range(start_id, start_id+len(df))))
    m.update_clean(df)

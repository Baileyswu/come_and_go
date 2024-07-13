import logging
from cg.manager import Manager
from cg.data_container import DataContainer
data = DataContainer.init('data/go')


def test_manager_head():
    m = Manager(data)
    logging.info(f'manager head \n{m.head}')
    df = m.get_head()
    df = m.get_head()
    m.update_head()
    df = m.get_head()


def test_manager_label():
    m = Manager(data)
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')


def test_manager_sweep():
    m = Manager(data)
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
    m.sweep()


def test_manager_skip():
    m = Manager(data)
    df = m.get_head()
    m.skip_label(df)

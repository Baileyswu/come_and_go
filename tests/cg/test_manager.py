import logging
from cg.manager import Manager

def test_manager_label():
    m = Manager('data/dirty.csv', 'data/clean.csv')
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')


def test_manager_head():
    m = Manager('data/dirty.csv', 'data/clean.csv')
    logging.info(f'manager head {m.head}')
    df = m.get_head()
    df = m.get_head()
    m.update_head()
    df = m.get_head()


def test_manager_sweep():
    m = Manager('data/dirty.csv', 'data/clean.csv')
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
    m.sweep()
import logging
from cg.manager import Manager

def test_manager_label():
    m = Manager('data/go')
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')


def test_manager_head():
    m = Manager('data/go')
    logging.info(f'manager head {m.head}')
    df = m.get_head()
    df = m.get_head()
    m.update_head()
    df = m.get_head()


def test_manager_sweep():
    m = Manager('data/go')
    df = m.get_head()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
    m.sweep()


def test_manager_skip():
    m = Manager('data/go')
    df = m.get_head()
    m.skip_label(df)


def test_manager_sub_cls():
    m = Manager('data/go').init_sub('WxManager')
    m.get_head()


def test_manager_decide_cls():
    m = Manager('data/go').decide_sub()
    logging.info(m.__class__.__name__)

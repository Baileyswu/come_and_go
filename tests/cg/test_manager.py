import logging
from cg.manager import Manager

def test_manager():
    m = Manager('data/dirty.csv', 'data/clean.csv')
    df = m.select_ones()
    m.get_label_and_move(df, '支出-交通-燃料/充电')
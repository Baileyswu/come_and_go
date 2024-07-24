import logging
from cg.plotter import Plotter

from cg.data_container import DataContainer


def test_plotter_month_line():
    data = DataContainer.init('data/go')
    p = Plotter(data)
    df, x, y, hue = p.month_stats(2024, '收入')
    logging.info(x)
    logging.info(y)
    logging.info(hue)
    logging.info(f'\n{df}')


def test_month_detail():
    data = DataContainer.init('data/go')
    p = Plotter(data)
    df = p.month_detail(2024, 6, '日常生活')
    logging.info(f'\n{df}')
    logging.info(df.columns)

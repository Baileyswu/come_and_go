import logging
from cg.plotter import Plotter

from cg.data_container import DataContainer
data = DataContainer.init('data/go')


def test_plotter_month_line():
    p = Plotter(data)
    df, x, y, hue = p.month_stats(2024, '收入')
    logging.info(x)
    logging.info(y)
    logging.info(hue)
    logging.info(f'\n{df}')

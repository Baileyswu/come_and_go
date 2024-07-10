import logging
from cg.plotter import Plotter


def test_plotter_month_line():
    p = Plotter('data/go')
    data, x, y, hue = p.month_stats(2024, '收入')
    logging.info(x)
    logging.info(y)
    logging.info(hue)
    logging.info(f'\n{data}')

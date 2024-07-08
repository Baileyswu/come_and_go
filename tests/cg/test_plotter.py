import logging
from cg.plotter import Plotter

def test_plotter_month_line():
    p = Plotter('data/go')
    data, x, y = p.month_stats(2024)
    logging.info(x)
    logging.info(y)
    logging.info(data)
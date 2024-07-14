import logging
from cg.data_container import DataContainer
from cg.manager import Manager
from cg.plotter import Plotter


def test_data_sub_cls():
    d = DataContainer.init_sub('WxData', folder_path='data/go')
    logging.info(d.get_clean_size())


def test_data_decide_cls():
    m = DataContainer.init('data/go')
    logging.info(m.__class__.__name__)


def test_shared_data():
    data = DataContainer.init('data/go')
    m = Manager(data)
    p = Plotter(data)
    logging.info(m.data.get_clean_size())
    logging.info(p.data.get_clean_size())
    m.data.clean = m.data.clean.head(10)
    logging.info(data.get_clean_size())
    logging.info(m.data.get_clean_size())
    logging.info(p.data.get_clean_size())
    assert m.data.get_clean_size() == p.data.get_clean_size()
    assert m.data.get_skip_size() == p.data.get_skip_size()
    assert m.data.get_dirty_size() == p.data.get_dirty_size()


def test_get_methods():
    data = DataContainer.init('data/go')
    logging.info(data.get_years())
    logging.info(data.get_months(2024))

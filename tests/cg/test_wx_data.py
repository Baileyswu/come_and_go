import logging
from cg.wx_data import WxData


def test_manager_label():
    d = WxData('data/go')
    logging.info(d.get_clean_size())

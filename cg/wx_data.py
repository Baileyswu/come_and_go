import logging
from .data_container import DataContainer


class WxData(DataContainer):
    def __init__(self, folder_path) -> None:
        logging.info(f'==>init {__class__.__name__}<==')
        super().__init__(folder_path)

    def init_dirty(self):
        super().init_dirty()
        self.dirty['金额'] = self.dirty['金额(元)'].apply(lambda x: float(x[1:]))
        self.dirty['商品说明'] = self.dirty['商品']

    def init_skip(self):
        sk = self.dirty[(self.dirty['收/支'] == '不计收支') |
                        (self.dirty['交易类型'] == '转入零钱通-来自零钱')]
        self.add_skip(sk)
        self.remove_dirty(sk)
        self.save()

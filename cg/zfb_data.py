import logging
from .data_container import DataContainer


class ZfbData(DataContainer):
    def __init__(self, folder_path) -> None:
        logging.info(f'==>init {__class__.__name__}<==')
        super().__init__(folder_path)

    def init_skip(self):
        sk = self.dirty[(self.dirty['收/支'] == '不计收支') |
                        (self.dirty['交易状态'] == '交易关闭')]
        self.dirty, self.skip = self._move(sk, self.dirty, self.skip)
        self.save()

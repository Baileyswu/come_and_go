import pandas as pd
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .model import Model
from .log import logger
from .module import Module
from .data_container import DataContainer


class Manager(Module):

    def __init__(self, data: DataContainer) -> None:
        logger.info(f'==>init {__class__.__name__}<==')

        # 数据对象
        self.data = data

        # model
        self.model = Model()

        # static choice
        self.head = None
        self.update_head()
        self.show_cols = ['score', 'label', '日期', '金额', '交易对方', '备注']

        # warning
        self.warn_msg = None

    def update_head(self):
        logger.info('update self.head')
        if self.data.get_dirty_size() > 0:
            self.head = self.data.dirty.sample(1)
        else:
            logger.warning('no more dirty data')
            self.head = None

    def get_head(self):
        if self.head is None:
            logger.warning('get_head: head is None')
        else:
            logger.info(f'get_head:\n{self.head}')
        return self.head

    def sweep(self):
        logger.info('sweep...')
        sp = self.find_similar()
        if len(sp) == 0:
            logger.info('no more sweep')
            return None
        self._format_data(sp)
        sp = self._check_label(sp)
        self.data.add_clean(sp)
        self.data.remove_dirty(sp)
        self.data.save()
        return sp[self.show_cols]

    def get_label_and_move(self, df: pd.DataFrame, label):
        logger.info('get_label_and_move...')
        df['label'] = label
        df['score'] = 1
        self._format_data(df)
        df = self._check_label(df)
        self.data.add_clean(df)
        self.data.remove_dirty(df)
        self.data.save()
        return df[self.show_cols]

    def skip_label(self, df: pd.DataFrame):
        '''把一些不打标的数据直接转移到skip中'''
        logger.info('skip_label...')
        self.data.add_skip(df)
        self.data.remove_dirty(df)
        self.data.save()

    def find_similar(self):
        self.model.train(self.data.clean)
        self.model.predict(self.data.dirty)
        similar = self.data.dirty.query('score > 0.8')
        return similar

    def _format_data(self, df):
        if len(df) == 0:
            logger.warning('_format_data null')
            return None
        group = df['label'].apply(lambda x: x.split('-'))
        dtime = pd.to_datetime(df['交易时间'])
        df['收支'] = group.apply(lambda x: x[0])
        df['分类'] = group.apply(lambda x: x[1])
        df['子分类'] = group.apply(lambda x: x[2])
        df['日期'] = dtime.dt.date
        df['月份'] = dtime.dt.month
        df['年份'] = dtime.dt.year
        df['备注'] = df['商品说明']
        logger.info(f'formated:\n{df}')
        return df

    def _check_label(self, df: pd.DataFrame):
        tmp = df[df['收/支'] != df['label'].apply(lambda x: x[:2])]
        df = df.drop(tmp.index)
        if len(df) == 0:
            self.warn_msg = f'conflict 收/支\n{tmp[self.show_cols]}'
            logger.warning(self.warn_msg)
            return df
        return df

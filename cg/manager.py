import warnings
import pandas as pd
import logging
from .tools import save_data, load_cache
from .model import Model
from .log import logger

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

class Manager(object):

    def __init__(self, dirty_path, clean_path) -> None:
        logger.info('==>init manager<==')
        self.dirty = load_cache(dirty_path)
        self.clean = load_cache(clean_path)
        logger.info(f'clean_size: {self.get_clean_size()}')
        logger.info(f'dirty_size: {self.get_dirty_size()}')
        self.dirty_path = dirty_path
        self.clean_path = clean_path
        self.label_set = self._get_label_set(self.clean)
        self.cat_set = self._get_cat_set(self.clean)
        self.dirty['score'] = 0
        self.dirty['label'] = None
        self.model = Model()
        self.head = None
        self.update_head()
        # self.sweep()

    def get_label_set(self):
        return self._get_label_set(self.clean)

    def _get_label_set(self, df: pd.DataFrame):
        assert '分类' in df.columns and '子分类' in df.columns, '先填入分类和子分类'
        df['子分类'] = df['子分类'].fillna('null')
        df['label'] = df['收支'] + '-' + df['分类'] + '-' + df['子分类']
        return df['label'].value_counts().index
    

    def _get_cat_set(self, df: pd.DataFrame):
        tmp = df['收支'] + '-' + df['分类']
        return tmp.value_counts().index


    def get_dirty_size(self):
        return len(self.dirty) if self.dirty is not None else 0


    def update_head(self):
        logger.info('update self.head')
        if len(self.dirty) > 0:
            self.head = self.dirty.sample(1)
        else:
            logger.warning('no more dirty data')
            self.head = None


    def get_head(self):
        if self.head is None:
            logger.warning('get_head:head is None')
        else:
            logger.info(f'get_head:\n{self.head}')
        return self.head


    def get_clean_size(self):
        return len(self.clean) if self.clean is not None else 0


    def find_similar(self, df):
        dc = self.clean[self.clean.id.isin(df.id.tolist())]
        return dc


    def _save_clean(self):
        save_data(self.clean, self.clean_path)


    def _save_dirty(self):
        save_data(self.dirty, self.dirty_path)


    def sweep(self):
        logger.info('sweep...')
        logger.info(f'clean_size: {self.get_clean_size()}')
        logger.info(f'dirty_size: {self.get_dirty_size()}')
        self.model.train(self.clean)
        self.model.predict(self.dirty)
        sp = self.dirty[self.dirty.score > 0.9]
        self._format_data(sp)
        self._move(sp)
        self._save()
        return sp


    def get_label_and_move(self, df:pd.DataFrame, label):
        logger.info('get_label_and_move...')
        df['label'] = label
        self._format_data(df)
        self._move(df)
        self._save()
        return df[['日期', '金额', '收支', '分类', '子分类', '备注']]


    def _move(self, df:pd.DataFrame):
        if len(df) == 0: return None
        self.clean = pd.concat([self.clean, df], axis=0, ignore_index=True)
        self.dirty = self.dirty.drop(df.index)


    def _save(self):
        self._save_clean()
        self._save_dirty()


    def _format_data(self, df):
        if len(df) == 0: return None
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
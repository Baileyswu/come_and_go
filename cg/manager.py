import pandas as pd
from .tools import save_data, load_cache
from .model import Model
from .log import logger

class Manager(object):

    def __init__(self, dirty_path, clean_path) -> None:
        self.dirty = load_cache(dirty_path)
        self.clean = load_cache(clean_path)
        logger.info(f'clean_size: {self.get_clean_size()}')
        logger.info(f'dirty_size: {self.get_dirty_size()}')
        self.dirty_path = dirty_path
        self.clean_path = clean_path
        self.label_set = self.get_label_set(self.clean)
        self.dirty['score'] = 0
        self.dirty['label'] = None
        self.model = Model()
        # self.sweep()

    def get_label_set(self, df: pd.DataFrame):
        assert '分类' in df.columns and '子分类' in df.columns, '先填入分类和子分类'
        df['子分类'] = df['子分类'].fillna('null')
        df['label'] = df['收支'] + '-' + df['分类'] + '-' + df['子分类']
        return df.label.value_counts().index

    def get_dirty_size(self):
        if self.dirty is None:
            return 0
        return len(self.dirty)
    
    def get_clean_size(self):
        if self.clean is None:
            return 0
        return len(self.clean)
    
    def select_ones(self):
        logger.info('select_ones...')
        df = self.dirty.sort_values('score').head(1)
        return df
    
    def find_similar(self, df):
        dc = self.clean[self.clean.id.isin(df.id.tolist())]
        return dc
    
    def save_clean(self):
        self.clean = save_data(self.clean, self.clean_path)

    def save_dirty(self):
        self.dirty = save_data(self.dirty, self.dirty_path)

    def sweep(self):
        logger.info('sweep...')
        logger.info(f'clean_size: {self.get_clean_size()}')
        logger.info(f'dirty_size: {self.get_dirty_size()}')
        self.model.train(self.clean)
        self.model.predict(self.dirty)
        sp = self.dirty[self.dirty.score > 0.9]
        self.format_data(sp)
        self.move(sp)
        return sp
        
    def get_label_and_move(self, df:pd.DataFrame, label):
        logger.info('get_label_and_move...')
        df['label'] = label
        self.format_data(df)
        self.move(df)
        return df[['日期', '金额', '收支', '分类', '子分类', '备注']]
    
    def move(self, df):
        logger.info('move...')
        if len(df) == 0: return None
        self.clean = pd.concat([self.clean, df], axis=0)
        self.dirty = self.dirty.drop(df.index)

        self.save_clean()
        self.save_dirty()
    
    def format_data(self, df):
        logger.info('format_data...')
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
        return df
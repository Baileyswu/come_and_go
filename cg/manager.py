import pandas as pd
from .tools import save_data, load_cache
from .model import Model

class Manager(object):

    def __init__(self, dirty_path, clean_path) -> None:
        self.dirty = load_cache(dirty_path)
        self.clean = load_cache(clean_path)
        self.dirty_path = dirty_path
        self.clean_path = clean_path
        self.label_set = self.get_label_set(self.clean)
        self.dirty['score'] = 0
        self.dirty['label'] = None
        self.model = Model()
        self.sweep()

    def get_label_set(self, df: pd.DataFrame):
        assert '分类' in df.columns and '子分类' in df.columns, '先填入分类和子分类'
        df['子分类'] = df['子分类'].fillna('null')
        df['label'] = df['收支'] + '-' + df['分类'] + '-' + df['子分类']
        return df.label.value_counts().index

    def get_dirty_size(self):
        return len(self.dirty)
    
    def get_clean_size(self):
        return len(self.clean)
    
    def select_ones(self):
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
        self.model.train(self.clean)
        self.dirty['score'] = self.model.predict(self.dirty)
        sp = self.dirty[self.dirty.score > 0.9]
        self.clean = pd.concat([self.clean, sp], axis=0)
        self.dirty = self.dirty.drop(sp.index)
        
    def get_label_and_move(self, df:pd.DataFrame, label):
        group = label.split('-')
        dtime = pd.to_datetime(df['交易时间'])
        df['label'] = label
        df['收支'] = group[0]
        df['分类'] = group[1]
        df['子分类'] = group[2]
        df['日期'] = dtime.dt.date
        df['月份'] = dtime.dt.month
        df['年份'] = dtime.dt.year
        df['备注'] = df['商品说明']

        self.clean = pd.concat([self.clean, df], axis=0)
        self.dirty = self.dirty.drop(df.index)

        self.save_clean()
        self.save_dirty()
        return df[['日期', '金额', '收支', '分类', '子分类', '备注']]
import pandas as pd
from .tools import save_data, load_cache
from .model import Model

class Manager(object):

    def __init__(self, dirty_path, clean_path) -> None:
        self.dirty = load_cache(dirty_path)
        self.clean = load_cache(clean_path)
        self.dirty_path = dirty_path
        self.clean_path = clean_path
        if 'score' not in self.dirty.columns:
            self.dirty['score'] = 0

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
        save_data(self.clean, self.clean_path)

    def save_dirty(self):
        save_data(self.dirty, self.dirty_path)

    def sweep(self):
        model = Model()
        model.train(self.clean)
        self.dirty['score'] = model.predict(self.dirty)
        sp = self.dirty[self.dirty.score > 0.9]
        self.clean = pd.concat([self.clean, sp], axis=0)
        self.dirty = self.dirty.drop(sp.index)
        
    def get_label(self, df, label):
        df['label'] = label
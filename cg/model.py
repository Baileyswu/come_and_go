import pandas as pd
from .tools import create_pd_dict
class Model(object):
    def __init__(self) -> None:
        self.params = {}

    def train(self, df: pd.DataFrame):
        assert '交易对方' in df.columns and 'label' in df.columns, '交易对方 和 label 不存在'
        stats = df[['交易对方', 'label']].fillna('')
        stats = stats.value_counts()
        stats = stats[stats > 1].reset_index()
        self.params = create_pd_dict(stats, '交易对方', 'label')

    def predict(self, df:pd.DataFrame):
        df['label'] = df['交易对方'].apply(lambda x: self.params.get(x))
        df['score'] = df['label'].apply(lambda x: 1 if x is not None else 0)
import pandas as pd
from .tools import create_pd_dict


class Model(object):
    def __init__(self) -> None:
        self.params = {}

    def train(self, df: pd.DataFrame):
        assert '交易对方' in df.columns and 'label' in df.columns, '交易对方 和 label 不存在'
        stats = df[['交易对方', 'label']].fillna('')
        stats = stats.value_counts().reset_index()

        # 对一个交易方的多个标签进行分组求和并计算比率，大于0.9则认为交易方和标签为直接的映射关系
        total_by_count = stats.groupby('交易对方')['count'].transform('sum')
        stats['score'] = stats['count'] / total_by_count
        truth = stats[stats['score'] > 0.5]
        self.params = create_pd_dict(truth, '交易对方', 'label')
        self.scores = create_pd_dict(truth, '交易对方', 'score')

    def predict(self, df: pd.DataFrame):
        df['label'] = df['交易对方'].map(self.params)
        df['score'] = df['交易对方'].map(self.scores)

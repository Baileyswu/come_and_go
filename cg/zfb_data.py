import logging
import pandas as pd
from .data_container import DataContainer
from .tools import save_data, append_path_file


class ZfbData(DataContainer):
    def __init__(self, folder_path) -> None:
        logging.info(f'==>init {__class__.__name__}<==')
        super().__init__(folder_path)

    def init_skip(self):
        # 无法标注的数据根据规则直接加入到skip，待后期处理
        sk = self.dirty[(self.dirty['收/支'] == '不计收支') |
                        (self.dirty['交易状态'] == '交易关闭')]
        self.add_skip(sk)
        self.remove_dirty(sk)

        # 交易关闭不再计入
        dp = self.skip[(self.skip['交易状态'] == '交易关闭')]
        self.remove_skip(dp)

        # 投资理财单独放一个文件
        asset = self.skip[self.skip['交易分类'] == '投资理财']
        if len(asset) > 0:
            # 注意第二遍写被覆盖为空
            save_data(asset, append_path_file(self.skip_path, 'asset.csv'))
            self.remove_skip(asset)

        # 退款处理
        assert (self.skip.value_counts('交易订单号') > 1).sum() == 0, '有重复退款的脏数据'
        # self.skip = self.skip.drop_duplicates('交易订单号')
        tk = self.skip[self.skip['交易状态'] == '退款成功']
        stats = tk[['商家订单号', '金额']].groupby('商家订单号').sum('金额').reset_index()\
            .rename(columns={'金额': '退款金额'})
        tmp = pd.merge(self.clean, stats, on='商家订单号', how='inner')
        tmp['金额'] = tmp['金额'] - tmp['退款金额']
        self.clean.loc[tmp.index, '金额'] = tmp['金额']

        # self.save()

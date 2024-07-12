import matplotlib.pyplot as plt
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .log import logger
from .manager import Manager

# 设置matplotlib的字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


class Plotter(object):
    def __init__(self, mg: Manager) -> None:
        logger.info(f'==>init {__class__.__name__}<==')
        self.mg = mg

    def month_stats(self, year, io):
        df = self.mg.clean.query(' 年份 == @year and 收支 == @io ')
        stats = df.groupby(['月份', '分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        return stats[['月份', '分类', '金额']], '月份', '金额', '分类'

    def month_sub_stats(self, year, cat):
        df = self.mg.clean.query(' 年份 == @year and 分类 == @cat ')
        stats = df.groupby(['月份', '子分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        return stats[['月份', '子分类', '金额']], '月份', '金额', '子分类'

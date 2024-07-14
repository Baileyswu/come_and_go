import matplotlib.pyplot as plt
from cg.echarts import bar_stack, pie
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .log import logger
from .data_container import DataContainer

# 设置matplotlib的字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


class Plotter(object):
    def __init__(self, data: DataContainer) -> None:
        logger.info(f'==>init {__class__.__name__}<==')
        self.data = data

    def month_stats(self, year, io):
        df = self.data.clean.query(' 年份 == @year and 收支 == @io ')
        stats = df.groupby(['月份', '分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        bar_stack(stats[['月份', '分类', '金额']], '月份', '金额', '分类')
        return stats[['月份', '分类', '金额']], '月份', '金额', '分类'

    def month_sub_stats(self, year, cat):
        df = self.data.clean.query(' 年份 == @year and 分类 == @cat ')
        stats = df.groupby(['月份', '子分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        bar_stack(stats[['月份', '子分类', '金额']], '月份', '金额', '子分类')
        return stats[['月份', '子分类', '金额']], '月份', '金额', '子分类'

    def month_detail(self, year, month, cat):
        df = self.data.clean.query(
            '年份 == @year and 月份 == @month and 分类 == @cat')
        stats = df.groupby('子分类').sum()['金额'].astype(int).reset_index()
        stats = stats.sort_values('金额')
        pie(stats, '子分类', '金额')
        return df.sort_values('金额', ascending=False)

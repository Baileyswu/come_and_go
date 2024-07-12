import matplotlib.pyplot as plt
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .log import logger

# 设置matplotlib的字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


class Plotter(object):
    def __init__(self, folder_path) -> None:
        logger.info(f'==>init {__class__.__name__}<==')

        # 数据存储
        self.folder_path = folder_path
        self.clean_path = '/'.join([folder_path, 'clean.csv'])
        self.skip_path = '/'.join([folder_path, 'skip.csv'])
        self.clean = load_cache(self.clean_path)
        self.skip = load_cache(self.skip_path)

        self._init_clean()

    def _init_clean(self):
        self.clean['money'] = self.clean.apply(
            lambda r: r['金额'] if r['收支'] == '收入' else -r['金额'], axis=1)

    def month_stats(self, year, io):
        df = self.clean.query(' 年份 == @year and 收支 == @io ')
        stats = df.groupby(['月份', '分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        return stats[['月份', '分类', '金额']], '月份', '金额', '分类'

    def month_sub_stats(self, year, cat):
        df = self.clean.query(' 年份 == @year and 分类 == @cat ')
        stats = df.groupby(['月份', '子分类']).sum('金额').reset_index()
        stats['金额'] = stats['金额'].astype(int)
        return stats[['月份', '子分类', '金额']], '月份', '金额', '子分类'

    def reload_file(self):
        logger.info('reloading file')
        self.clean = load_cache(self.clean_path)
        self.skip = load_cache(self.skip_path)

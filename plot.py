import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 设置matplotlib的字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


def plot_all():
    df = pd.read_csv('data/feishu.csv')
    stats = df.groupby(['年份', '收支']).sum('金额').reset_index()
    plot_year_line(stats, 'years.png', '所有年份收支情况')


def plot(year):
    df = pd.read_csv('data/feishu.csv')
    df['money'] = df.apply(lambda r: r['金额'] if r['收支']=='收入' else -r['金额'], axis=1)
    stats = df.groupby(['年份', '月份', '分类', '子分类']).sum('money').reset_index()

    plot_month_line(stats[stats['年份']==year], f'{year}.png', f'{year}年各类支出情况')


def plot_month_line(df:pd.DataFrame, save_path, title='plot_month_line'):
    param = {
        'df': df,
        'save_path': save_path,
        'width': 3,
        'cat': '分类',
        'x': '月份',
        'y': '金额',
        'hue': '子分类',
        'figsize': (5, 5),
        'title': title,
    }
    sub_plot(**param)


def plot_year_line(df:pd.DataFrame, save_path, title):
    param = {
        'df': df,
        'save_path': save_path,
        'width': 1,
        'cat': '收支',
        'x': '年份',
        'y': '金额',
        'figsize': (5, 5),
        'title': title,
    }
    sub_plot(**param)


def sub_plot(df, save_path, width, cat, x, y, hue=None, figsize=(5,4), title=None):
    cats = df[cat].drop_duplicates().tolist()

    height = (len(cats)-1) // width + 1  # 向上取整
    fig, axes = plt.subplots(height, width, figsize=(figsize[0]*width, figsize[1]*height))

    for i in range(len(cats)):
        col = cats[i]
        sub = df[df[cat] == col]
        ax = get_axes_pos(axes, width, height, i//width, i%width)
        px = sns.barplot(data=sub, x=x, y=y, hue=hue, ax=ax, legend='full')
        px.set_title(col)
    logging.info(f'save plotting to {save_path}')
    fig.suptitle(title)
    plt.savefig(save_path, dpi=300)


def get_axes_pos(axes, width, height, x, y):
    if height == 1:
        return axes[y]
    if width == 1:
        return axes[x]
    return axes[x, y]

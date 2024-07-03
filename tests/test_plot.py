import pandas as pd
from plot import plot_month_line, plot_year_line, plot, plot_all

def test_plot_month_line():
    df = pd.read_csv('data/feishu.csv')
    df['money'] = df.apply(lambda r: r['金额'] if r['收支']=='收入' else -r['金额'], axis=1)
    stats = df.groupby(['年份', '月份', '分类', '子分类']).sum('money').reset_index()

    plot_month_line(stats[stats['年份']==2023], '2023.png')


def test_plot_year_line():
    df = pd.read_csv('data/feishu.csv')
    stats = df.groupby(['年份', '收支']).sum('金额').reset_index()

    plot_year_line(stats, 'years.png')


def test_plot_year():
    plot(2024)
    plot_all()
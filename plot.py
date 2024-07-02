import logging
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 设置matplotlib的字体，以便在图表中显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题


def plot_month_line(df:pd.DataFrame, save_path):

    cats = df['分类'].drop_duplicates().tolist()

    width = 3
    height = (len(cats)-1) // width + 1  # 向上取整
    fig, axes = plt.subplots(height, width, figsize=(5*width, 4*height))

    for i in range(len(cats)):
        col = cats[i]
        sub = df[df['分类'] == col]
        ax = get_axes_pos(axes, height, i//width, i%width)
        sns.barplot(data=sub, x='月份', y='金额', hue='子分类', ax=ax, legend='full')
    logging.info(f'save plotting to {save_path}')
    plt.savefig(save_path, dpi=300)


def get_axes_pos(axes, height, x, y):
    if height <= 1:
        return axes[y]
    return axes[x, y]
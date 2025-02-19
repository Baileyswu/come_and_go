import pandas as pd
from .log import logger
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .module import Module


class DataContainer(Module):
    def __init__(self, folder_path) -> None:
        logger.info(f'==>init {__class__.__name__}<==')

        # 数据存储
        self.folder_path = folder_path
        self.dirty_path = '/'.join([folder_path, 'dirty.csv'])
        self.clean_path = '/'.join([folder_path, 'clean.csv'])
        self.skip_path = '/'.join([folder_path, 'skip.csv'])
        self.dirty = load_cache(self.dirty_path)
        self.clean = load_cache(self.clean_path)
        self.skip = load_cache(self.skip_path)
        self.init_dirty()
        self.init_clean()
        self.init_skip()

        # label
        self.label_set = self.get_label_set()
        self.cat_set = self.get_cat_set()

    def init(folder_path):
        '''
        根据数据列名知晓账单来源，初始化对应的解析器
        '''
        dirty_path = '/'.join([folder_path, 'dirty.csv'])
        header = load_cache(dirty_path, head=0).columns

        if is_contains(header, ['交易时间', '交易分类', '交易对方', '对方账号', '商品说明', '收/支', '金额', '收/付款方式', '交易状态',
                                '交易订单号', '商家订单号', '备注']):
            return DataContainer.init_sub('ZfbData', folder_path=folder_path)
        if is_contains(header, ['交易时间', '交易类型', '交易对方', '商品', '收/支', '金额(元)', '支付方式', '当前状态', '交易单号',
                                '商户单号', '备注']):
            return DataContainer.init_sub('WxData', folder_path=folder_path)
        return DataContainer(folder_path)

    def reload(self):
        logger.info('reloading file')
        self.dirty = load_cache(self.dirty_path)
        self.clean = load_cache(self.clean_path)
        self.skip = load_cache(self.skip_path)

    def save_clean(self):
        save_data(self.clean, self.clean_path)

    def save_dirty(self):
        save_data(self.dirty, self.dirty_path)

    def save_skip(self):
        save_data(self.skip, self.skip_path)

    def save(self):
        logger.info('saving files')
        self.save_clean()
        self.save_dirty()
        self.save_skip()

    def init_dirty(self):
        self.dirty['score'] = 0
        self.dirty['label'] = None

    def init_clean(self):
        pass

    def init_skip(self):
        pass

    def get_label_set(self):
        df = self.clean
        assert '分类' in df.columns and '子分类' in df.columns, '先填入分类和子分类'
        df['子分类'] = df['子分类'].fillna('null')
        df['label'] = df['收支'] + '-' + df['分类'] + '-' + df['子分类']
        return df['label'].value_counts().index.tolist()

    def get_cat_set(self):
        return self.clean['分类'].value_counts().index.tolist()

    def get_years(self):
        return self.clean['年份'].drop_duplicates().tolist()

    def get_months(self, year):
        df = self.clean.query('年份 == @year')
        return df['月份'].drop_duplicates().tolist()

    def get_dirty_size(self):
        return len(self.dirty) if self.dirty is not None else 0

    def get_clean_size(self):
        return len(self.clean) if self.clean is not None else 0

    def get_skip_size(self):
        return len(self.skip) if self.skip is not None else 0

    def add_clean(self, df: pd.DataFrame):
        if len(df) > 0:
            logger.info(f'add\n{df}')
            self.clean = pd.concat([self.clean, df], axis=0, ignore_index=True)

    def add_skip(self, df: pd.DataFrame):
        if len(df) > 0:
            logger.info(f'add\n{df}')
            self.skip = pd.concat([self.skip, df], axis=0, ignore_index=True)

    def remove_dirty(self, df: pd.DataFrame):
        if len(df) > 0:
            logger.info(f'remove\n{df}')
            self.dirty = self.dirty.drop(df.index)

    def remove_clean(self, ids):
        if len(ids) > 0:
            logger.info(f'remove {ids}')
            self.clean = self.clean.drop(ids)

    def remove_skip(self, df: pd.DataFrame):
        if len(df) > 0:
            logger.info(f'remove\n{df}')
            self.skip = self.skip.drop(df.index)

    def format_data(self, df: pd.DataFrame):
        if len(df) == 0:
            logger.warning('format_data null')
            return None
        logger.info('format data')
        if '交易时间' in df.columns:
            dtime = pd.to_datetime(df['交易时间'])
            df['日期'] = dtime.dt.date
            df['月份'] = dtime.dt.month
            df['年份'] = dtime.dt.year
        if '商品说明' in df.columns:
            df['备注'] = df['商品说明']
        if 'label' in df.columns:
            group = df['label'].apply(lambda x: x.split('-'))
            df['收支'] = group.apply(lambda x: x[0])
            df['分类'] = group.apply(lambda x: x[1])
            df['子分类'] = group.apply(lambda x: x[2])
        logger.info(f'formated:\n{df}')
        return df

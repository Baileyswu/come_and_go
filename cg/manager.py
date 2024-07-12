import warnings
import pandas as pd
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .model import Model
from .log import logger
from .module import Module

warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


class Manager(Module):

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
        self._init_dirty()
        self._init_clean()
        self._init_skip()

        # label
        self.label_set = self._get_label_set(self.clean)
        self.cat_set = self._get_cat_set(self.clean)

        # model
        self.model = Model()

        # static choice
        self.head = None
        self.update_head()
        self.show_cols = ['score', 'label', '日期', '金额', '交易对方', '备注']

        # warning
        self.warn_msg = None

    def decide_sub(folder_path):
        '''
        根据数据列名知晓账单来源，初始化对应的解析器
        '''
        dirty_path = '/'.join([folder_path, 'dirty.csv'])
        header = load_cache(dirty_path, head=0).columns

        if is_contains(header, ['交易时间', '交易类型', '交易对方', '商品', '收/支', '金额(元)', '支付方式', '当前状态', '交易单号',
                                '商户单号', '备注']):
            return Manager.init_sub('WxManager', folder_path=folder_path)
        if is_contains(header, ['交易时间', '交易分类', '交易对方', '对方账号', '商品说明', '收/支', '金额', '收/付款方式', '交易状态',
                                '交易订单号', '商家订单号', '备注']):
            return Manager.init_sub('ZfbManager', folder_path=folder_path)
        return Manager(folder_path)

    def get_label_set(self):
        logger.info('get_label_set')
        return self._get_label_set(self.clean)

    def reload_file(self):
        logger.info('reloading file')
        self.dirty = load_cache(self.dirty_path)
        self.clean = load_cache(self.clean_path)
        self.skip = load_cache(self.skip_path)

    def get_dirty_size(self):
        return len(self.dirty) if self.dirty is not None else 0

    def get_clean_size(self):
        return len(self.clean) if self.clean is not None else 0

    def get_skip_size(self):
        return len(self.skip) if self.skip is not None else 0

    def update_head(self):
        logger.info('update self.head')
        if len(self.dirty) > 0:
            self.head = self.dirty.sample(1)
        else:
            logger.warning('no more dirty data')
            self.head = None

    def get_head(self):
        if self.head is None:
            logger.warning('get_head:head is None')
        else:
            logger.info(f'get_head:\n{self.head}')
        return self.head

    def sweep(self):
        logger.info('sweep...')
        self.model.train(self.clean)
        self.model.predict(self.dirty)
        sp = self.dirty[self.dirty.score > 0.8]
        if len(sp) == 0:
            logger.info('no more sweep')
            return None
        self._format_data(sp)
        sp = self._check_label(sp)
        self.dirty, self.clean = self._move(sp, self.dirty, self.clean)
        self._save()
        return sp[self.show_cols]

    def get_label_and_move(self, df: pd.DataFrame, label):
        logger.info('get_label_and_move...')
        df['label'] = label
        df['score'] = 1
        self._format_data(df)
        df = self._check_label(df)
        self.dirty, self.clean = self._move(df, self.dirty, self.clean)
        self._save()
        return df[self.show_cols]

    def skip_label(self, df: pd.DataFrame):
        logger.info('skip_label...')
        self.dirty, self.skip = self._move(df, self.dirty, self.skip)
        self._save()

    def find_similar(self, df):
        dc = self.clean[self.clean.id.isin(df.id.tolist())]
        return dc

    def _save_clean(self):
        save_data(self.clean, self.clean_path)

    def _save_dirty(self):
        save_data(self.dirty, self.dirty_path)

    def _save_skip(self):
        save_data(self.skip, self.skip_path)

    def _move(self, df: pd.DataFrame, source, target):
        if len(df) == 0:
            logger.warning('_move null')
            return source, target
        target = pd.concat([target, df], axis=0, ignore_index=True)
        source = source.drop(df.index)
        return source, target

    def _save(self):
        logger.info('saving files')
        self._save_clean()
        self._save_dirty()
        self._save_skip()

    def _format_data(self, df):
        if len(df) == 0:
            logger.warning('_format_data null')
            return None
        group = df['label'].apply(lambda x: x.split('-'))
        dtime = pd.to_datetime(df['交易时间'])
        df['收支'] = group.apply(lambda x: x[0])
        df['分类'] = group.apply(lambda x: x[1])
        df['子分类'] = group.apply(lambda x: x[2])
        df['日期'] = dtime.dt.date
        df['月份'] = dtime.dt.month
        df['年份'] = dtime.dt.year
        df['备注'] = df['商品说明']
        logger.info(f'formated:\n{df}')
        return df

    def _get_label_set(self, df: pd.DataFrame):
        assert '分类' in df.columns and '子分类' in df.columns, '先填入分类和子分类'
        df['子分类'] = df['子分类'].fillna('null')
        df['label'] = df['收支'] + '-' + df['分类'] + '-' + df['子分类']
        return df['label'].value_counts().index

    def _get_cat_set(self, df: pd.DataFrame):
        tmp = df['收支'] + '-' + df['分类']
        return tmp.value_counts().index

    def _init_dirty(self):
        self.dirty['score'] = 0
        self.dirty['label'] = None

    def _init_clean(self):
        pass

    def _init_skip(self):
        pass

    def _check_label(self, df):
        tmp = df[df['收/支'] != df['label'].apply(lambda x: x[:2])]
        df = df.drop(tmp.index)
        if len(df) == 0:
            self.warn_msg = f'conflict 收/支\n{tmp[self.show_cols]}'
            logger.warning(self.warn_msg)
            return df
        return df

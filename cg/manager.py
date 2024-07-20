import pandas as pd
from .tools import save_data, load_cache, create_pd_dict, is_contains
from .model import Model
from .log import logger
from .module import Module
from .data_container import DataContainer


class Manager(Module):

    def __init__(self, data: DataContainer) -> None:
        logger.info(f'==>init {__class__.__name__}<==')

        # 数据对象
        self.data = data

        # model
        self.model = Model()

        # static choice
        self.head = None
        self.update_head()
        self.show_cols = ['score', 'label', '日期', '金额', '交易对方', '备注']

        # warning
        self.warn_msg = None

    def update_head(self):
        logger.info('update self.head')
        if self.data.get_dirty_size() > 0:
            self.head = self.data.dirty.sample(1)
        else:
            logger.warning('no more dirty data')
            self.head = None

    def get_head(self):
        if self.head is None:
            logger.warning('get_head: head is None')
        else:
            logger.info(f'get_head:\n{self.head}')
        return self.head

    def sweep(self):
        logger.info('sweep...')
        sp = self.find_similar()
        if len(sp) == 0:
            logger.info('no more sweep')
            return None
        self.data.format_data(sp)
        sp = self._check_label(sp)
        self.data.add_clean(sp)
        self.data.remove_dirty(sp)
        self.data.save()
        return sp[self.show_cols]

    def get_label_and_move(self, df: pd.DataFrame, label):
        logger.info('get_label_and_move...')
        df['label'] = label
        df['score'] = 1
        self.data.format_data(df)
        df = self._check_label(df)
        self.data.add_clean(df)
        self.data.remove_dirty(df)
        self.data.save()
        return df[self.show_cols]

    def update_clean(self, changes: dict, idx: list):
        logger.info('update clean')

        add_rows = changes.get('added_rows')
        edited_rows = changes.get('edited_rows')
        deleted_rows = changes.get('deleted_rows')

        if edited_rows is not None and len(edited_rows) > 0:
            edited_rows = {idx[k]: v for k, v in edited_rows.items()}
            self._edit_data(edited_rows)
        if add_rows is not None and len(add_rows) > 0:
            self._add_data(add_rows)
        if deleted_rows is not None and len(deleted_rows) > 0:
            deleted_rows = [idx[i] for i in deleted_rows]
            self._delete_data(deleted_rows)

        # 保存数据
        self.data.save_clean()

    def skip_label(self, df: pd.DataFrame):
        '''把一些不打标的数据直接转移到skip中'''
        logger.info('skip_label...')
        self.data.add_skip(df)
        self.data.remove_dirty(df)
        self.data.save()

    def find_similar(self):
        self.model.train(self.data.clean)
        self.model.predict(self.data.dirty)
        similar = self.data.dirty.query('score > 0.8')
        return similar

    def _check_label(self, df: pd.DataFrame):
        tmp = df[df['收/支'] != df['label'].apply(lambda x: x[:2])]
        df = df.drop(tmp.index)
        if len(df) == 0:
            self.warn_msg = f'conflict 收/支\n{tmp[self.show_cols]}'
            logger.warning(self.warn_msg)
            return df
        return df

    def _edit_data(self, rows):
        '''编辑修改'''
        logger.info('_edit_data')
        for idx, row in rows.items():
            for name, value in row.items():
                self.data.clean.loc[self.data.clean.index[idx], name] = value

    def _delete_data(self, row):
        '''删除'''
        logger.info('_delete_data')
        self.data.remove_clean(row)

    def _add_data(self, rows):
        '''增加'''
        logger.info('_add_data')
        start_id = self.data.clean.index.max() + 1
        df = pd.DataFrame(rows).set_index(
            pd.Index(range(start_id, len(rows)+start_id)))
        df = self.data.format_data(df)
        self.data.add_clean(df)

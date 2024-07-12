import inspect
import os
import pandas as pd
import numpy as np
import logging
# import yaml

FILLNA_VALUE = -99


def split_dataset(df, label, by='time'):
    '''
    分割数据集
    by=time 按时间分割，取最后3000条
    by=rate 按比例划分，20%作为测试集
    '''
    logging.info('splitting dataset ...')
    logging.info(f'fillna={FILLNA_VALUE}')
    df = df.fillna(FILLNA_VALUE)

    if len(df) < 3000:
        by = 'rate'
        logging.info('df len < 3000, use rate=0.2 to split data for debug')

    if by == 'rate':
        df_train = df.sample(frac=0.8, random_state=23)
        df_test = df.drop(df_train.index)
    elif by == 'time':
        df_test = df[-3000:]
        df_train = df.drop(df_test.index)

    X_train, y_train = cut_columns(df_train, label)
    X_test, y_test = cut_columns(df_test, label)

    return (X_train, y_train), (X_test, y_test)


def cut_columns(df, label):
    X = df[[i for i in df.columns.tolist() if i not in [label]]]  # 训练集
    y = df[label]
    return X, y


def data_split(data_source, num_processes):
    '''数据分块'''
    sec = int(num_processes)
    split_dfs = np.array_split(data_source, sec)
    return split_dfs


def convert2int(lst: list):
    return [int(i) for i in lst if i != '']


def dict_get_key(dt: dict, key: str):
    if isinstance(dt, dict) is False:
        logging.warning('dict not exists')
        return None
    value = dt.get(key)
    if value is None and key != 'default':
        logging.warning(f'cannot find key:{key}, set default value')
        return dict_get_key(dt, 'default')
    logging.debug(f'dict_get_key: {key} -> {value}')
    return value


def get_default(value, default):
    '''当value为None时填充默认值default'''
    if value is None:
        return default
    return value


def create_pd_dict(df, key, value):
    '''通过dataframe中的两列生成字典'''
    return df.set_index(key)[value].to_dict()


def load_cache(path: str, head=None):
    logging.info(f'loading cache from: {path}')
    if path is None:
        logging.error('path is None')
        return pd.DataFrame({})
    if os.path.exists(path):
        if path.endswith(".csv"):
            header = pd.read_csv(path, nrows=0).columns
            # 保留原始index进行对齐
            if 'Unnamed: 0' in header:
                return pd.read_csv(path, index_col=0, nrows=head)
            return pd.read_csv(path, nrows=head)
        # elif path.endswith(".json"):
        #     from common.json_util import read_json
        #     return read_json(path)
        # elif path.endswith(".yaml") or path.endswith(".yml"):
        #     return load_yaml(path)
        else:
            logging.warning('check file post')
    logging.info('cache not exists')
    return pd.DataFrame({})


def save_data(data, path: str = None):
    logging.info(f'saving data to {path}')
    logging.info(f'tot: {len(data)}')
    if path is None or len(path) == 0:
        logging.warning('file not saved!')
    try:
        if path.endswith(".csv"):
            data.to_csv(path, encoding='utf-8-sig')
        # elif path.endswith(".yaml") or path.endswith('.yml'):
        #     save_settings_to_yaml(data, path)
        # elif path.endswith('.json'):
        #     from common.json_util import write_json
        #     write_json(data, path)
    except OSError as e:
        logging.error(e)
        if 'non-existent' in str(e):
            parent, _ = os.path.split(path)
            logging.info(f'makedirs: {parent}')
            os.makedirs(parent, exist_ok=True)
            save_data(data, path)
    except Exception as e:
        logging.error(e)
    return data


def log_feature_complete_rate(df: pd.DataFrame):
    stats = 1-df.isna().sum()/len(df)
    stats = stats.sort_values()
    stats = stats[stats.lt(1)].to_dict()
    logging.info(f'feature complete rate(<1): {stats}')


def count_repeat(lst):
    from collections import Counter
    cs = Counter(lst)
    repeats = [col for col, count in cs.items() if count > 1]
    return repeats


def show_custom_names(module):
    return [name for name in dir(module) if not name.startswith("__")]


def show_module_attr_values(module):
    '''获取模块中所有属性和方法的名字'''
    attributes = dir(module)

    # 使用字典推导式获取每个属性或方法的名称及对应的值
    variables_dict = {
        attr: getattr(module, attr) for attr in attributes if not attr.startswith("__") and not callable(getattr(module, attr))}

    return variables_dict


def get_class_methods(cls):
    '''返回类的所有属性和方法的列表'''
    # dir()函数返回类的所有属性和方法的列表
    all_attributes = dir(cls)

    # 过滤出以__开头和结尾的特殊方法，以及过滤掉继承自object的方法
    methods = [
        name for name in all_attributes if
        callable(getattr(cls, name)) and not name.startswith("__") and name != 'mro']

    return methods


# def save_settings_to_yaml(settings, path):
#     logging.info(f'saving setting to yaml: {path}')
#     try:
#         with open(path, 'w', encoding='utf-8') as f:
#             yaml.dump(settings, f, allow_unicode=True)
#     except Exception as e:
#         logging.error(e)


# def load_yaml(path):
#     '''通过导入yaml配置初始化strategy方法'''
#     logging.info(f'loading setting from {path}')
#     with open(path, 'r', encoding='utf-8') as file:
#         loaded_data = yaml.safe_load(file)
#     return loaded_data


def current_line_number():
    return inspect.currentframe().f_lineno


def is_contains(parent, children):
    for child in children:
        if child not in parent:
            return False
    return True

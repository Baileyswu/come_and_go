import logging


class Module(object):
    """模块基类
    """
    subclassdict = {}

    def __init_subclass__(cls):
        '''子类注册时生成映射表'''
        Module.subclassdict.update({cls.__name__: cls})
        logging.info(f'register: {cls.__name__}')

    def init_sub(name, **kwargs):
        '''通过name调用相应的子类'''
        try:
            cls = Module.subclassdict.get(name)
            if cls is not None:
                return cls(**kwargs)
            logging.warning(
                f'{name} not exists, use default base {__class__.__name__}')
            return Module(**kwargs)
        except Exception as e:
            logging.error(e)

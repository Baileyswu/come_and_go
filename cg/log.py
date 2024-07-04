import logging
import sys

# 创建一个 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# # 创建一个 handler，用于写入日志文件
# fh = logging.FileHandler('app.log')
# fh.setLevel(logging.DEBUG)

# # 再创建一个 handler，用于输出到控制台
# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)

# # 定义 handler 的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)

# # 给 logger 添加 handler
# logger.addHandler(fh)
# logger.addHandler(ch)

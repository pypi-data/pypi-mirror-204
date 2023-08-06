import logging
from termcolor import colored

logger = logging.getLogger('xjm_test_log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('/home/xjm/xjm/xjm_pycharm/Attribute_Explainable/xjm.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formater = logging.Formatter(fmt = colored("[%(asctime)s]",'green') +'--'+ colored("{- %(name)s}",'yellow' ) + "- %(levelname)s - %(message)s",datefmt = '%Y-%m-%d %H:%M:%S')

fh.setFormatter(formater)
ch.setFormatter(formater)

logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("debug message")
logger.info("info message")
logger.warning("warn message")
logger.error("error message")
logger.critical("critical message")


print('ok')
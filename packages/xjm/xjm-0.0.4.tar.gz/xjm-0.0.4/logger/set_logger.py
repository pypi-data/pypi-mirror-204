import logging
from termcolor import colored

def _set_log():
    logger = logging.getLogger('xjm_log')
    logger.setLevel(logging.DEBUG)

    ch_hander = logging.StreamHandler()
    fh_hander = logging.FileHandler('/home/wangyn/xjm/PFnet/xjm_logging_log')

    ch_hander.setLevel(logging.DEBUG)
    fh_hander.setLevel(logging.DEBUG)

    # fmt = '%(asctime)s %(name)s %filename)s %(lineno)d: %(levelname)s %(message)s'
    fmt = logging.Formatter("%(asctime)s - %(name)s  - line:%(lineno)d - %(levelname)s - %(message)s")
    color_fmt = colored('%(asctime)s %(name)s', 'green') + colored(' %(filename)s %(lineno)d', 'yellow') + ':%(levelname)s %(message)s'  #%filename)s
    ch_hander.setFormatter((logging.Formatter(fmt=color_fmt, datefmt='%Y-%m-%d %H:%M:%S')))
    # fh_hander.setFormatter(logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S'))
    # ch_hander.setFormatter(fmt)
    fh_hander.setFormatter(fmt)


    logger.addHandler(ch_hander)
    logger.addHandler(fh_hander)

    return logger
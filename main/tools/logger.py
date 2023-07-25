import time
import os

from config import setting

# calculate the path of the '../log/log.txt'
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# general log file name by current time 'yyyy-mm-dd.log.txt'
LOG_FILENAME = time.strftime('%Y-%m-%d.log.txt', time.localtime(time.time()))
LOG_FILE_PATH  = os.path.join(PROJECT_PATH, 'log', LOG_FILENAME)


def log(content, type='info'):
    """
    Log the content to the console
    args:
        content - the content to be logged
    return:
        None
    """

    content = str(content)

    with open(LOG_FILE_PATH, 'a+') as f:
        f.write('[%s] ' % type + content + '\n')


def log_print(content, type='info'):
    """
    Log the content to the console
    args:
        content - the content to be logged
    return:
        None
    """

    content = str(content)
    if setting.LOG_LEVEL > 0:
        print('[%s] ' % type + content)
    
    log(content, type)


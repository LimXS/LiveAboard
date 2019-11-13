#*-* coding:UTF-8 *-*
import logging.handlers
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
#print curPath

def addlogmes(logType, cases, message, LOG_FILE = curPath + "\log.txt"):
    # LOG_FILE='C:\\workspace\\nufeeb.pyt\\commondata\\testlog'
    #print LOG_FILE
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
    # fmt='%(asctime)s - %(filename)s:%(filename)s-%(funcName)s-%(lineno)s - %(name)s - %(levelname)s - %(message)s'
    fmt = '%(asctime)s - %(levelname)s - %(name)s  - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger(cases)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    if logType == 'info':
        logger.info(message)
    elif logType == 'debug':
        logger.debug(message)
    elif logType == 'error':
        logger.error(message)
    elif logType == 'warning':
        logger.warning(message)
    elif logType == 'critical':
        logger.critical(message)
    logger.removeHandler(handler)
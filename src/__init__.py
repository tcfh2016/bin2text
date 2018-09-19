# -*- coding: utf-8 -*-

import logging
import datetime
import pdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

timestamp = datetime.datetime.now()
log_file = ".\\log\\" + timestamp.strftime("%Y-%m-%d-%H-%M-%S") + ".log"
open(log_file, 'w').close()

pdb.set_trace()
logger_handler = logging.FileHandler(log_file)
logger_handler.setLevel(logging.DEBUG)

logger_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)
logger.info("Complete loger configuration!-->%s" % (log_file))

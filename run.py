#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2017-08-22 21:39:16

import logging
from scrapy.cmdline import execute


logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False
cmd = 'scrapy crawl hpoi'
execute(cmd.split())

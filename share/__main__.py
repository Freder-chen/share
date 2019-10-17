# -*- coding: utf-8 -*-

import os, sys
if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)


import share
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s : [%(levelname)s] %(message)s'
)

share.update()

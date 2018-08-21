# -*- coding: utf-8 -*-
from app import app

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


app.run(host='0.0.0.0', port='8080')
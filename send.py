#!/usr/bin/env python3

from datetime import datetime
import asyncore
import sys
import time
from smtpd import SMTPServer

import subprocess

PVT = sys.argv[1]

class Server (SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'),
            self.no)
        print(filename)
        f = open(filename, 'wb')
        f.write(data)
        f.close()
        print('%s saved.' % filename)
        cmd = ["freechains","--sign="+PVT,"chain","post","/mail","file","utf8",filename]
        print(' '.join(cmd))
        #time.sleep(2)
        subprocess.run(cmd)
        self.no += 1

Server(('localhost', 2525), None)
try:
    asyncore.loop()
except KeyboardInterrupt:
    pass

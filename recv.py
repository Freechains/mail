#!/usr/bin/env python3

USER  = "username"
CHAIN = "/mail"

"""
TODO
- periodic recv (via TB?)
- multiple chains
- set from, sign, hash, etc
- set mail account
"""

import os.path
import subprocess
import json

JSON  = 'state.json'
STATE = {
    'heads' : []
}

if not os.path.isfile(JSON):
    cmd  = ["freechains","chain","genesis",CHAIN]
    #print(' '.join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    gen  = proc.stdout.read().decode("utf-8").rstrip()
    assert gen != ''
    STATE['heads'] = [gen]
    with open(JSON,'w') as f:
        json.dump(STATE, f)

with open('state.json','r') as f:
    STATE = json.load(f)

olds = ' '.join(STATE['heads'])
cmd  = ["freechains","chain","traverse",CHAIN,"all",olds]
#print("cmd: " + ' '.join(cmd))
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

out = proc.stdout.read().decode("utf-8").rstrip()
if out == '':
    news = []
else:
    news = out.split(' ')

for h in news:
    print("receiving: " + h)
    cmd = ["freechains","chain","get",CHAIN,"payload",h]
    #print("cmd: " + ' '.join(cmd))
    proc = subprocess.Popen(cmd, bufsize=0,stdout=subprocess.PIPE)
    pay  = proc.stdout.read().decode("utf-8").rstrip()
    with open('tmp.eml','w') as f:
        f.write(pay)
    subprocess.run(["./eml2mbox.py","tmp.eml","/var/mail/"+USER])

proc  = subprocess.Popen(["freechains","chain","heads",CHAIN,"all"], stdout=subprocess.PIPE)
heads = proc.stdout.read().decode("utf-8").rstrip().split(' ')
STATE['heads'] = heads
with open(JSON,'w') as f:
    json.dump(STATE, f)

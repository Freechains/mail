#!/usr/bin/env python3

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
    cmd  = ["freechains","chain","genesis","/mail"]
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
cmd  = ["freechains","chain","traverse","/mail","all",olds]
#print("cmd: " + ' '.join(cmd))
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

out = proc.stdout.read().decode("utf-8").rstrip()
if out == '':
    news = []
else:
    news = out.split(' ')

for h in news:
    print("receiving: " + h)
    cmd = ["freechains","chain","get","/mail",h]
    #print("cmd: " + ' '.join(cmd))
    proc = subprocess.Popen(cmd, bufsize=0,stdout=subprocess.PIPE)
    js   = proc.stdout.read().decode("utf-8").rstrip()
    py  = json.loads(js)
    with open('tmp.eml','w') as f:
        f.write(py['pay'])
    subprocess.run(["./eml2mbox.py","tmp.eml","/var/mail/chico"])

proc  = subprocess.Popen(["freechains","chain","heads","/mail","all"], stdout=subprocess.PIPE)
heads = proc.stdout.read().decode("utf-8").rstrip().split(' ')
STATE['heads'] = heads
with open(JSON,'w') as f:
    json.dump(STATE, f)

#!/usr/bin/env python3

import os.path
import subprocess
import json

JSON  = 'state.json'
STATE = {
    'heads' : []
}

if not os.path.isfile(JSON):
    with open(JSON,'w') as f:
        json.dump(STATE, f)

with open('state.json','r') as f:
    STATE = json.load(f)

fc = subprocess.Popen(["freechains","chain","heads","linked","/mail"], stdout=subprocess.PIPE)
heads = fc.stdout.read().decode("utf-8").split()

for h in heads:
    if h in STATE['heads']:
        break
    print(h)
    fc = subprocess.Popen(["freechains","chain","get","/mail",h], stdout=subprocess.PIPE)
    js = fc.stdout.read()
    py = json.loads(js)
    with open('tmp.eml','w') as f:
        f.write(py['pay'])
    subprocess.run(["./eml2mbox.py","tmp.eml","/var/mail/chico"])

STATE['heads'] = heads
with open(JSON,'w') as f:
    json.dump(STATE, f)

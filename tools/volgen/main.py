import json,os
from math import pi

def fp(*args):
    return os.path.join(".",*args)

def vol(r,h):
    return pi*(r**2)*h

def main(*,outfp=fp("out.json"),infp=fp("in.json"),indent=2):
    global dat
    f=open(infp,"r+")
    dat=json.load(f)
    f.close()
    o={"coins":{},"ingots":{}}
    for k in dat['coins']:
        v=dat['coins'][k]
        if k!="units":
            v['volume']=vol(v['radius'],v['height'])
            o['coins'][k]=v
        else:
            o['coins'][k]=v
    for k in dat['ingots']:
        v=dat["ingots"][k]
        if k!="units":
            v['volume']=v['width']*v['length']*v['height']
            o['ingots'][k]=v
        else:
            o['ingots'][k]=v
    #print(json.dumps(o,indent=indent))
    f=open(outfp,"w+")
    f.write(json.dumps(o,indent=indent))
    f.close()

if __name__=="__main__":
    main()
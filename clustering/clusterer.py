import random
import tkinter as tk
import csv
with open("world_cup_in_out.csv") as f:
    reader=csv.reader(f)
    everything=list(reader)
    everything=list(map(lambda x: (float(x[0]),float(x[1])),everything))

def fcentroids(s):
    p=[]
    for c in range(s):
        p.append(everything[random.randint(0,len(everything))])
    return p

def eucdsq(a,b):
    x=a[0]-b[0]
    y=a[1]-b[1]
    distance=(x**2+y**2)
    return distance

def around(cents):
    psofeachc={}
    for c in cents:
        psofeachc[c]=[]
    for pair in everything:
        shortd=(1000000000,0)
        for c in cents:
            if eucdsq(c,pair)<shortd[0]:
                shortd=(eucdsq(c,pair),c)
        psofeachc[shortd[1]].append(pair)
    newcents=[]
    for key in psofeachc:
        tx=0
        ty=0
        n=0
        for pair in psofeachc[key]:
            tx+=pair[0]
            ty+=pair[1]
            n+=1
        if n!=0:
            newcents.append((tx/n,ty/n))
    return newcents

def hawkeye(cents):
    total=0
    for pair in everything:
        ds=[]
        for c in cents:
            ds.append(eucdsq(c,pair))
        total+=min(ds)
    return total

minivar = [[],1000000000]

for a in range(10):
    cents = fcentroids(5)
    while cents!=around(cents):
        cents=around(cents)
    if hawkeye(cents)<minivar[1]:
        minivar[1]=hawkeye(cents)
        minivar[0]=cents
    #print(hawkeye(cents))

print(minivar)

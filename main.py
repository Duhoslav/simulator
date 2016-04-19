# -*- coding: utf-8 -*-
__author__ = 'duhoslav'
import  json
import subprocess
import threading
import sys
import time

def cmd(programm,args,timeout=0):
    pr=subprocess.Popen("./"+programm+args,stdout=subprocess.PIPE,shell=True)
    print pr.stdout.read()
    time.sleep(timeout)

def run_in_threads(opt,timeout):
    threads_count=int(opt['threads'])
    for i in xrange(threads_count):
        thread=threading.Thread(target=cmd, args=[opt['programm'],opt['args']])
        thread.start()
        thread.join()
        time.sleep(timeout)

if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'Specify configeration file or use key "-help" for description.'
        exit()
    if len(sys.argv) > 2:
        print 'Too many arguments! Specify configeration file or use key "-help" for description.'
        exit()
    if sys.argv[1]=="-help":
        print '''Configuration file is a json object.
The main arguments are name, description (natural language) protocol and "options" array
In this array you can specify several tries - one json object per attack. Type delay, speed, threads , etc. in options object'''
        exit()

    file=open(sys.argv[1])
    d = json.load(file)
    for i in xrange(len(d['options'])):
        try:
            timeout = float(d['options'][i]['timeout'])
        except:
            timeout = 0
        if d['options'][i]['threads']:
            run_in_threads(d['options'][i],timeout/1000)
        else:
            cmd(d['options'][i]['programm'],d['options'][i]['args'],timeout/1000)

    file.close()

   # print d
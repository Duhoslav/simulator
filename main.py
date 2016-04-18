# -*- coding: utf-8 -*-
__author__ = 'duhoslav'
import  json
import subprocess
import threading
import time

def cmd(programm,args):
    pr=subprocess.Popen("./"+programm+args,stdout=subprocess.PIPE,shell=True)
    print pr.stdout.read()

def run_in_threads(opt,timeout):
    threads_count=int(opt['threads'])
    for i in xrange(threads_count):
        thread=threading.Thread(target=cmd, args=[opt['programm'],opt['args']])
        thread.start()
        thread.join()
        time.sleep(timeout)

if __name__ == '__main__':
    file=open('conf.json')
    d = json.load(file)

    for i in xrange(len(d['options'])):
        try:
            timeout=float(d['options'][i]['timeout'])
        except:
            timeout=0
        if d['options'][i]['threads']:
            run_in_threads(d['options'][i],timeout/1000)
    file.close()

   # print d
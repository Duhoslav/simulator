# -*- coding: utf-8 -*-
__author__ = 'duhoslav'
import  json
import subprocess
import threading
import sys
import time
import requests
import StringIO
import socket

def sniffer(port):
    try:
        s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        return None

    # receive a packet
    while True:
        packet = s.recvfrom(port)
        print packet

def cmd(programm,args,maxsize,timeout=0):
    #sniffer(65565)
    with open('listurl') as f:
        list_url=f.readlines()
    start_traffic_activity(list_url,maxsize)
    pr=subprocess.Popen("./"+programm+args,stdout=subprocess.PIPE,shell=True)
    #print pr.stdout.read()
    time.sleep(timeout)

def run_in_threads(opt,timeout):
    threads_count=int(opt['threads'])
    for i in xrange(threads_count):
        thread=threading.Thread(target=cmd, args=[opt['programm'],opt['args'],opt['legal_traffic_size']])
        thread.start()
        thread.join()
        time.sleep(timeout)

def start_traffic_activity(url_list,maxsize):
    for i in xrange(len(url_list)):
        r=requests.get(url_list[i], stream=True)
        size = 0
        ctt = StringIO()


        for chunk in r.iter_content(2048):
            size += len(chunk)
            ctt.write(chunk)
            if size > maxsize:
                r.close()
                raise ValueError('Response too large')
        content = ctt.getvalue()

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
            cmd(d['options'][i]['programm'],d['options'][i]['args'],d['legal_traffic_size'],timeout/1000)

    file.close()

   # print d
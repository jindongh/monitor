#!/usr/bin/python
#encoding: utf-8
#@author: jindongh@gmail.com
#@brief: check website and notify when content changed

import config
import os
import urllib

def main():
    #get new content
    url='http://www.hbhsxlz.cn/baoming/'
    webfd=urllib.urlopen(url)
    res=webfd.read()

    #get old content
    oldres=''
    oldfname='/tmp/yahao.bak'
    if os.path.exists(oldfname):
        oldfd=open(oldfname)
        oldres=oldfd.read()
        oldfd.close()

    #check chaneg
    if not oldres==res:
        config.sms('changed:%s' % url)
    else:
        config.log('%s not changed' % url)

    #save change
    fd=open(oldfname,'w')
    fd.write(res)
    fd.close()

if __name__=='__main__':
    main()


#!/usr/bin/python
#encoding: utf-8
#@author: jindongh@gmail.comf
#@brief: config

import os
import datetime
import fetion

def log(msg, log_type='common'):
    log_file='%s/%s.log' % (dir_log(), log_type)
    open(log_file, 'a').write('%s %s\n' % (datetime.datetime.now(), msg))

def sms(msg, user='18201614369'):
    sms=fetion.Fetion()
    sms.setuser('18201614369','mypassword')
    sms.sendsms(user, msg)

def dir_data():
    return '%s/data/' % dir_top()

def dir_log():
    return '%s/log/' % dir_top()

def dir_top():
    return '%s' % os.path.dirname(os.path.abspath(__file__))

if __name__=='__main__':
    log('hello')


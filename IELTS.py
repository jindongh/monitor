#!/usr/bin/env python
#encoding: utf-8
import urllib,urllib2,cookielib
import time,zlib,re,md5
import sys
import json
import config
import fetion
class Site:
        debug=True
        #创建Cookie
        def __init__(self):
                cj=cookielib.LWPCookieJar()
                opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                opener.addheaders=[('User-agent','Opera/9.23')]
                urllib2.install_opener(opener)
        # 登录校内网
        def login(self, userId, userPwd):
		self.req('http://ielts.etest.net.cn/login')
                url="http://ielts.etest.net.cn/login"
                body=(("userId",userId),("userPwd",userPwd),("checkImageCode",""))
                res = self.req(url,body)
		if self.debug:
			open('%s/login.res' % config.dir_data(),'a').write(res)
        # 请求网页的工具函数，直接返回网页内容
        def req(self,url,body=()):
                if len(body)==0:
                        req=urllib2.Request(url)
                else:
                        req=urllib2.Request(url,urllib.urlencode(body))
			config.log('%s?%s' % (url, urllib.urlencode(body)))
		try:
			raw=urllib2.urlopen(req)
		except:
			config.log('access %s failed' % url)
			sys.exit(1)
                return raw.read()
	def checkSeat(self):
		#130527200212051639
		body=(("queryMonths","2014-04"),("queryProvinces",11),("_",int(time.time()*1000)))
		url="http://ielts.etest.net.cn/myHome/1968462/queryTestSeats?%s" % urllib.urlencode(body)
		req = urllib2.Request(url)
		req.add_header('Accept','text/html,application/xhtml+xml,application/xml,application/json')
		req.add_header('X-Requested-With','XMLHttpRequest')
		try:
			raw = urllib2.urlopen(req)
		except:
			config.log('access %s failed' % url)
			sys.exit(1)
		res = raw.read()
		if self.debug:
			open('%s/seats.res' % config.dir_data(),'a').write(res)
		obj = json.loads(res)
		seats=[]
		seatNum=0
		if not type(obj) is dict:
			open('%s/bad.res' % config.dir_data(), 'a').write(res)
			config.log('check seats failed')
			return seats
		for day in obj.keys():
			for center in obj[day]:
				seatNum+=1
				if center['levelCode']=='A/G' and center['optStatus']==1:
					seats.append(center['seatGuid'])
		config.log('%d seats found from %d seats' % (len(seats), seatNum))
		if not 0==len(seats):
			self.sms('trying')
		return seats
	def bookSeat(self, sid):
		url='http://ielts.etest.net.cn/myHome/1968462/createOrderConfirm'
		body=(('seatGuid',sid),)
		res=self.req(url,body)
		if self.debug:
			open('%s/book.res' % config.dir_data(),'a').write(res)
		url='http://ielts.etest.net.cn/myHome/1968462/newAppointment'
		body=(('seatGuid',sid),)
		res = self.req(url,body)
		if self.debug:
			open('%s/confirm.res' % config.dir_data(),'a').write(res)
	def sms(self, msg):
		sms=fetion.Fetion()
		sms.setuser('18201614369','mypassword')
		sms.sendsms('18201614369','IELTS_got_seat_%s' % msg)

if __name__=='__main__':
	site = Site()
	site.login("1968462","96a48d0738fb4fe43598090fac6597bb")
	seats = site.checkSeat()
	for seat in seats:
		site.bookSeat(seat)


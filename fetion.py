#coding:utf-8
#调用飞信
 
import urllib2
import urllib
 
class Fetion:
    msisdn = ''
    passwd = ''
    baseurl = 'http://quanapi.sinaapp.com/fetion.php'
    #设置登陆用户
    def setuser(self,msisdn,passwd):
        self.msisdn = msisdn
        self.passwd = passwd
 
    #发送短信
    def sendsms(self,recmsisdn,content):
        cod = 1
        if self.msisdn == '' :
            cod = 0
            return 'msisdn is null'
        if self.passwd == '' :
            cod = 0
            return 'passwd is null'
        if recmsisdn == '' :
            cod = 0
            return 'recmsisdn is null'
        if content == '':
            cod = 0
            return 'content is null'
        if cod == 1 :
            smsurl = self.baseurl + '?u=' + self.msisdn + '&p=' + self.passwd + '&to='+recmsisdn +'&m=' + content
            print smsurl
            res = urllib2.urlopen(smsurl).read()
            print res
            #反馈调用结果
            return res.split(',')[0].split(':')[1]
if __name__=='__main__':
    newfetion = Fetion()
    #设置登陆飞信的用户
    newfetion.setuser('18201614369','mypassword')
    #发送短信
    print newfetion.sendsms('18201614369','测试')


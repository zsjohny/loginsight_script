#-*- coding: utf-8 -*
'''
Author:         wanghe 
Email:          wangh@loginsight.cn
Author website: 
 
File: jinja2_test.py
Create Date: 2016-04-12 21:56:58
''' 
def dca():
    import urllib2
    response = urllib2.urlopen('http://7xslrj.com2.z0.glb.clouddn.com/IntermediateCA.crt')
    html = response.read()
if __name__ == '__main__':
    dca()
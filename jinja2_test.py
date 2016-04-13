#-*- coding: utf-8 -*
'''
Author:         wanghe 
Email:          wangh@loginsight.cn
Author website: 
 
File: jinja2_test.py
Create Date: 2016-04-12 21:56:58
''' 

from jinja2 import Template
import os

# with open("./nxlog.conf.tpl", "r") as fd:
#     content = fd.read(4096)
#     # print 'content = ', content
#     template = Template(content)
#     HELLO = raw_input('inout:\n')
#     HELLO2 = raw_input('inout2:\n')
#     HELLO3 = raw_input('inout3:\n')
#     alist = [{
#         'LOG_NAME': HELLO
#     }, {
#         'LOG_NAME': HELLO2
#     }, {
#         'LOG_NAME': HELLO3
#     }]
#
#     # nxlog_config = raw_input('Please input your nxlog path(default: /etc/nxlog):\n')
#     # nxlog_config_list = nxlog_config.split()
#     # nxlog_config_list =[str(a) for a in nxlog_config_list]
#     a = template.render(input_list=alist)
#     print a

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
import socket

host_name = socket.gethostname()
print(socket.gethostname())

def custom_config():
    raw_input('Press any key to continue..\n')
    nxlog_config = '/etc/nxlog'
    cert_dir = raw_input("Please input your CA path:\n")
    log_name = raw_input("Please input your log name:\n")
    log_path = raw_input("Please input your log path:\n")
    streamkey = raw_input("Please input your streamkey:\n")
    streamtype = raw_input("Please input your streamtype:\n")
    streamtag = raw_input("Please input your streamtag:\n")

    #todo: will add this varible to jinja


    with open("./nxlog.conf.tpl", "r") as fd:
        content = fd.read(4096)
        # print 'content = ', content
        template = Template(content)


        var_dict = [{
            'LOG_NAME': log_name
        }, {
            'LOG_PATH': log_path
        }, {
            'HOSTNAME': host_name
        }, {
            'STREAMKEY': streamkey
        }, {
            'SREAMTYPE': streamtype
        }, {
            'STREAMTAG': streamtag
        }, {
            'NXLOG_CONFIG_DIR': nxlog_config
        }, {
            'CERTDIR': cert_dir
        }]

        a = template.render(input_list=var_dict)
        print a


if __name__ == "__main__":
    custom_config = custom_config()
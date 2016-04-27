#!/usr/bin/env python2
#-*-encoding:utf-8-*-
import base64
import os
import platform
#from jinja2 import Template
import socket
import time
import sys
import shlex
import  requests
import  getpass

#http://www.loginsight.cn/o/applications/2/
CLIENT_ID = "1S_wRvye9?Xq4mU91e!MPixJ9Qjl3yQIaW?7G=2j"
CLIENT_SECRET = "hLXU?HCktQu::1xz9EsjWMUq:yiLp2A=SgQpH4HKTgM4zFS@WMQjFtVGSYV.gu6wC!6UCgfxSqyzKUZWymuyQq_lUGQH;Udmhy3gvAQ73GNF3HXgzT94YkNP0RvIx:m1"

# 用户名和密码
username = str(raw_input('please input your usrname:\n'))
password = str(getpass.getpass('please input your password:\n'))
host_type = str(raw_input('please input your will add host type(e.g. web):\n'))
url = "http://auth.loginsight.cn/o/token/"
headers = {"Authorization": "Basic " + base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)}
nxlog_data_path = '/etc/nxlog/data'
host_name = socket.gethostname()
platform_info = platform.system()
sys_type = platform.linux_distribution()[0]

def get_access_token():
    import requests
    # 请求oauth access token
    print '\n\nget access token ...'
    r = requests.post(url, data={'grant_type': 'password', 'username': username, 'password':password}, headers=headers)
    access_token = r.json()
    return access_token


def registered():
    import requests
    access_token = get_access_token()
    print 'access_token ==', access_token
    headers = {"Authorization": access_token['token_type'] + " " + access_token['access_token']}

    # 获取sentry 实例
    # 向sentry 实例注册主机
    data = {'host_name': host_name, 'host_type': host_type, 'system': platform_info, 'distver': '1.0',
            'mac_addr': "ff-cc-cd-20-21-21"}
    r = requests.post(url="http://app.loginsight.cn/api/0/agent/hosts", data=data, headers=headers)
    host_key = r.json()['host_key']
    return host_key
    color_print('注册成功!', 'blue')


def custom_config():
    from jinja2 import Template
    host_key = registered()
    raw_input('Press any key to continue..\n')
    nxlog_config = '/etc/nxlog'
    tpl_file = './nxlog.conf.tpl'
    output_file = '%s/nxlog.conf' % nxlog_config
    cert_dir = '%s/CA' % (nxlog_data_path)
    #log_name = raw_input("Please input your log name:\n")

    log_path = raw_input("Please input your log path:\n")
    streamkey = raw_input("Please input your streamkey:\n")
    streamtype = raw_input("Please input your streamtype:\n")
    streamtag = raw_input("Please input your streamtag:\n")


    with open(tpl_file, "r") as fd:
        content = fd.read(4096)
        # print 'content = ', content
        template = Template(content)


    kwargs = {
    'LOG_PATH': log_path,
    'HOSTNAME': host_key,
    'STREAMKEY': streamkey,
    'SREAMTYPE': streamtype,
    'STREAMRAG': streamtag,
    'CERTDIR': cert_dir,
    'NXLOG_CONFIG_DIR': nxlog_config,
    'CERTDIR': cert_dir
    }

    a = template.render(**kwargs)
    print a
    with open(output_file,'w') as f:
        f.write(a)


    # if len(nxlog_config) == 0 or len(cert_dir) == 0 or len(log_name) == 0 or len(log_path) == 0 or len(host_name) == 0 or len(tag) == 0:
    #     print("Please input corrent path")
    # else:
    #     os.environ['nxlog_config'] = str(nxlog_config)
    #     os.environ['cert_dir'] = str(cert_dir)
    #     os.environ['log_name'] = str(log_name)
    #     os.environ['log_path'] = str(log_path)
    #     os.environ['host_name'] = str(host_name)
    #     os.environ['tag'] = str(tag)
    #     #The follow is result
    #     os.system('echo $nxlog_config')
    #     os.system('echo $cert_dir')
    #     os.system('echo $log_name')
    #     os.system('echo $log_path')
    #     os.system('echo $host_name')
    #     os.system('echo $tag')



if __name__ == "__main__":
    custom_config = custom_config()
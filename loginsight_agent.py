#!/usr/bin/env python2
#-*-encoding:utf-8-*-
"""
Loginsight agent scripts
"""


#从安装源或我们的服务器下载nxlog
#能够完成oauth认证
#能够从服务器中取得host_key
#扫描/var/log
#能够添加监控的日志文件
#能够对归档日志文件做监控
#生成nxlog配置文件


import requests
import base64
import os
import platform
from jinja2 import Template
import socket

CLIENT_ID = "1S_wRvye9?Xq4mU91e!MPixJ9Qjl3yQIaW?7G=2j"
CLIENT_SECRET = "hLXU?HCktQu::1xz9EsjWMUq:yiLp2A=SgQpH4HKTgM4zFS@WMQjFtVGSYV.gu6wC!6UCgfxSqyzKUZWymuyQq_lUGQH;Udmhy3gvAQ73GNF3HXgzT94YkNP0RvIx:m1"

# 用户名和密码
# username='test'
# password = '123qwe'

username = 'test'
#username = raw_input('please input your username:\n')
password = '123qwe'
#password = raw_input('please input your passwd:\n')
host_name = socket.gethostname()
print(socket.gethostname())

url = "http://auth.loginsight.cn/o/token/"
headers = {"Authorization": "Basic " + base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)}

def install_source_code():
    platform_info = platform.system()
    sys_type = platform.linux_distribution()[0]

    if platform_info == "linux":
        if sys_type == "Ubuntu":
            os.system('sudo apt-get install  libdbi1 libapr1 libperl5.18  -y')
            os.chdir('/tmp')
            os.system('wget https://nxlog.co/system/files/products/files/1/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
            os.system('sudo dpkg -i nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
        elif sys_type == "Redhat" or sys_type =="Centos":
            os.system('yum install -y libdbi1 libapr1 libperl5.18')
            os.chdir('/tmp')
            os.system('https://nxlog.co/system/files/products/files/1/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm')
            os.system('yum -ivh nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm')
        else:
            print "You linux system not support."
    elif platform_info== "Darwin" or platform_info== "Windows":
         print "You script just for linux."

#fixme: will download config

def get_access_token():
    # 请求oauth access token
    print '\n\nget access token ...'
    r = requests.post(url, data={'grant_type': 'password', 'username': username, 'password':password}, headers=headers)
    print r.text
    access_token = r.json()
    return access_token


def scan_logs():
    if os.path.exists("/var/log"):
        for default_logfile in os.listdir("/var/log"):
            if default_logfile.endswith("log"):
                return default_logfile
                #todo: will add this to dict and caliing it on jinja
                #print(default_logfile)

def custom_logfile():
    raw_input('Press any key to continue..\n')
    nxlog_config = '/etc/nxlog'
    cert_dir = raw_input("Please input your CA path:\n")
    log_name = raw_input("Please input your log name:\n")
    log_path = raw_input("Please input your log path:\n")
#    host_name = raw_input("Please input your hostname:\n")
    streamkey = raw_input("Please input your tags(e.g. tag1,tag2):\n")
    streamtype = raw_input("Please input your tags(e.g. tag1,tag2):\n")
    streamtag = raw_input("Please input your tags(e.g. tag1,tag2):\n")

    #todo: will add this varible to jinja


    with open("./nxlog.conf.tpl", "r") as fd:
    content = fd.read(4096)
    # print 'content = ', content
    template = Template(content)

    # Exec    $HostName = {{ e.HOSTNAME }};
    # Exec    $StreamKey = {{ e.STREAMKEY }};
    # Exec    $StreamType = {{ e.SREAMTYPE }};
    # Exec    $StreamTag = {{ e.STREAMRAG }} ;

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
    }]

    a = template.render(input_list=var_dict)
    print a


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
    custom_logfile = custom_logfile()
    install_source_code = install_source_code()
    print '%s ==', install_source_code, install_source_code
    access_token = get_access_token()
    print '%s ==', access_token
    headers = {"Authorization": access_token['token_type'] + " " + access_token['access_token']}

    # 获取sentry 实例
    # 向sentry 实例注册主机
    data = {'host_name': 'testhost1', 'host_type': 'web1', 'system': 'linux', 'distver': '1.0', 'mac_addr': "ff-cc-cd-20-21-21" }
    r = requests.post(url="http://app.loginsight.cn/api/0/agent/hosts", data=data, headers=headers)
    print 'registered success!', r.text


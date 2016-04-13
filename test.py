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
import platform

host_name = socket.gethostname()
platform_info = platform.system()
sys_type = platform.linux_distribution()[0]

def main():
    if platform_info == "Linux" or platform_info == "linux" :
        if sys_type == "Ubuntu":
            os.system('sudo apt-get install  libdbi1 libapr1 libperl5.18 -y')
            os.chdir('/tmp')
            os.system('wget https://nxlog.co/system/files/products/files/1/nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
            os.system('sudo dpkg -i nxlog-ce_2.9.1504_ubuntu_1404_amd64.deb')
        elif sys_type == "Redhat" or sys_type =="Centos":
            os.system('yum install -y libdbi1 libapr1 libperl5.18 pip')
            os.chdir('/tmp')
            os.system('https://nxlog.co/system/files/products/files/1/nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm')
            os.system('yum -ivh nxlog-ce-2.9.1504-1_rhel6.x86_64.rpm')
        else:
            print "You linux system not support."
    elif platform_info == "Windows":
        print "Please read and install window docs."
    else:
        print "Not support to mac"

if __name__ == '__main__':
    main()
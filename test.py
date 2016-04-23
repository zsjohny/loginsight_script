import os

def ca():
    nxlog_data_path = '/tmp'
    pathisexists = os.path.exists(nxlog_data_path)
    ca_file = 'CA.tar.gz'
    ca_username = 'loginsight'
    ca_passwd = 'loginsight'
    Auth = '%s:%s' % (ca_username, ca_passwd)
    ca_url = 'http://%s@download.loginsight.cn/%s' % (Auth, ca_file)


    os.system('wget -P %s %s' % (nxlog_data_path, ca_url))
    os.system('tar fvxz %s/%s -C %s' % (nxlog_data_path, ca_file, nxlog_data_path))


if __name__ == '__main__':

    ca()
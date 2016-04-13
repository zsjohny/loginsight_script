#conding:utf-8
'''
this python script is used to initial syslog env and set on-off different log types

'''
import sys
from subprocess import Popen,PIPE,call
import platform
import os

def get_os():
	'''
	'''
	# cmd1=r'lsb_release -a'
	cmd2=r'cat /etc/issue'
	cmd3=r'uname -a'

	ret=Popen(cmd2,shell=True,stdout=PIPE)

	if 'Ubuntu 14.04' in t[0]:
		return 'Ubuntu14.04'

	ret=Popen(cmd3,shell=True,stdout=PIPE)
	t=ret.stdout.readlines()
	if 'el7' in t[0]:
		return 'CentOS7'
	if 'el6' in t[0]:
		return 'CentOS6'
	return False
def check_os(os_info):
	'''
	check host os
	'''
	ret=False
	support_name=['Linux','Ubuntu','CentOS','Redhat']
	for sname in support_name:
		if sname in os_info:
			return sname
	return False

def get_hostname():
	'''
	check
	'''
	info=platform.uname()
	hostname=info[1]
	return hostname

def check_hostname():
	'''
	'''
	hostname=get_hostname()
	if hostname:
		return True
	else:
		return False

def check_privilege():
	import os
	if os.geteuid() != 0:
		return False
	else:
		return True

def check_network(server_ip):
	'''
	'''
	IP=server_ip
	cmd=r'ping -c 1  -w 1 '+IP
	try:
		ret=Popen(cmd,shell=True,stdout=PIPE)
	except:
		return False
	return True

def check_auto_rsyslog():
	'''
	'''
	return True

def set_choice_rsyslog(osname,USER_KEY):
	'''
	'''

	# rule_file_name=r'50-default.conf'
	print osname
	os_dict={'Ubuntu14.04':r'/etc/rsyslog.conf','CentOS6':r'/etc/rsyslog.conf','CentOS7':r'/etc/rsyslog.conf'}
	sub_module=r'rsyslog.d'
	server_ip_port=r'192.168.70.104:514'
	server_ip_port2=r'192.168.70.106:10514'
	show_map_list={1:'auth',2:'cron',3:'daemon',4:'kern',5:'lpr',6:'mail',8:'user',7:'news'}
	suffix_string=r'@@'+server_ip_port
	another_suffix_string=r'@@'+server_ip_port2
	file_path=os_dict[osname]

	sub_conf_name='/'.join(file_path.split('/')[:-1])+'/'+sub_module+'/'
	type_list=dict()
	stat=0

	try:
		# print file_path
		stat=bakup_conf(file_path)
	except:
		print 'bakup syslog conf fail! \nplease check permission\n'
		exit(1)

	if stat:
		type_list={'auth':0,'cron':0,'daemon':0,'kern':0,'lpr':0,'mail':0,'user':0,'news':0}
		print '\n'*100+r'bakup origin file to:'+'\n'+' '*5+file_path+'.old\n'
		type_list={'auth':0,'cron':0,'daemon':0,'kern':0,'lpr':0,'mail':0,'user':0,'news':0}

	else:
		type_=['auth','cron','daemon','kern','lpr','mail','user','news']
		type_list={'auth':0,'cron':0,'daemon':0,'kern':0,'lpr':0,'mail':0,'user':0,'news':0}


		f=open(file_path,'r+')
		m=f.readlines()
		for item in type_:
			line=item+r'.* '+suffix_string+'\n'
			if line in m:
				type_list[item]=1
		f.close()

	cmd=r'cat '+file_path
	ret=Popen(cmd,shell=True,stdout=PIPE)
	content=ret.stdout.readlines()
	print_on_of_dict(type_list)
	while True:
		user_choice=raw_input('choose a item log type to operate:\n')
		if len(user_choice)==1:
			if user_choice.isdigit():
				if int(user_choice)==9:
					print 'maneage other log conf\n'

					'''recover origin file '''
					cmd_a=r'rm '+file_path
					cmd_b=r'cp '+file_path+'.old'+' '+file_path
					cmd_c=r'rm '+file_path+'.old'
					call(cmd_a,shell=True,stdout=PIPE)
					call(cmd_b,shell=True,stdout=PIPE)
					call(cmd_c,shell=True,stdout=PIPE)
					print 'origin conf file had been recovered...exit'
					break
				if int(user_choice)==0:
					break

				choice_type=show_map_list[int(user_choice)]

				set_choice(choice_type,type_list,file_path,suffix_string)

			elif user_choice.isalpha():
				if user_choice=='r':
					'''recover origin file '''
					cmd_a=r'rm '+file_path
					cmd_b=r'cp '+file_path+'.old'+' '+file_path
					cmd_c=r'rm '+file_path+'.old'
					call(cmd_a,shell=True,stdout=PIPE)
					call(cmd_b,shell=True,stdout=PIPE)
					call(cmd_c,shell=True,stdout=PIPE)
					print 'origin conf file had been recovered...exit'
					break
				if user_choice=='q':
					break
				if user_choice=='a':

					'''
					geng gai #imfile
					'''

					save_file=''
					t=list()
					ok=False
					while not ok:
						map_dict={
						'ip':server_ip_port2.split(':')[0],
						'port':server_ip_port2.split(':')[1],
						'filepath':'filepath',
						'ruleset_name':'ruleset_name',
						'tag':'tag',
						}
						# print 'append new log type to the rsyslog conf file\n '
						raw_input('Press any key to continue..\n')

						input_1=raw_input('log type name(e.g. nginx):\n')
						# map_dict['$InputFileTag']=input_1
						# map_dict['$InputFileStateFile']='state_'+input_1
						map_dict['tag']=input_1
						map_dict['ruleset_name']=input_1+'rule'
						input_2=raw_input('log file absolute path(e.g. /var/log/nginx*.log):\n')
						# map_dict['$InputFileName']=input_12
						map_dict['filepath']=input_2
						# new_log_field=['$InputFileTag','$InputFileName','$InputFileStateFile',\
						# '$InputFileSeverity','$InputFilePersistStateInterval',\
						# '$InputRunFileMonitor']

						fp=	sub_conf_name

						save_file=fp+map_dict['tag']+r'.conf'
						# print 'sentences below will be save into a file:%s\n'%(save_file)

						# long_sentence=""
						# for x in new_log_field:
						# 	# print x,map_dict[x]
						# 	long_sentence+=x+' '*2+map_dict[x]+'\n'
						# t.append(long_sentence)

						# #add  $WorkDirectory /var/lib/rsyslog
						# t.append(r'$WorkDirectory /var/lib/rsyslog'+'\n')
						t=make_user_manual_conf(map_dict)
						print t
						print '\n'
						print '|'+'--'*9+'|'
						print ('|  make sure? y/n  |')
						print '|'+'--'*9+'|'
						input_3=raw_input('\n')
						print '\n'

						# template_a=r'LogInsight_format'
						# # template_b=r"<%pri%>%protocol-version% %timestamp:::date-rfc3339% %HOSTNAME% %app-name% %procid% %msgid% [{user_key} tag=\"TAG\"] %msg%".format(user_key=USER_KEY)
						# template_b=r"<%pri%>[{user_key}] %msg%".format(user_key=USER_KEY)
						# template='$template '+template_a+','+r'"'+template_b+r'"'
						# button1=r'if $programname == '+r"'"+map_dict['$InputFileTag']+ r"'"+r'then %s;'%(suffix_string)+template_a+'\n'
						# button2=r"if $programname == "+r"'"+map_dict['$InputFileTag']+ r"'"+r'then %s;'%(another_suffix_string)+template_a+'\n'

						# button3=r"if $programname == "+r"'"+map_dict['$InputFileTag']+ r"'" +r'then ~'+'\n'

						# t.append('\n')
						# t.append(template)
						# t.append('\n')
						# t.append(button1)
						# t.append(button2)
						# t.append(button3)
						# t=''.join(t)
						if input_3=='y' or input_3=='Y':
							ok=True
						else:
							pass
						if ok:
							break
					try:
						f=open(save_file,'w+')

						# f.write(r'$ModLoad imfile'+'\n')
						f.write(t)
						'key add to be done'
					except:
						f.close()
						print 'create new file %s fail \n'%(save_file)


			else:
				print 'incorrect choice'
		else:
			print 'incorrect choice'
		print_on_of_dict(type_list)

	return True

def make_user_manual_conf(input_dict):
	ruleset_name=input_dict['ruleset_name']
	ip=input_dict['ip']
	port=input_dict['port']
	tag=input_dict['tag']
	filepath=input_dict['filepath']

	ttt='''
module(load="imfile" )
ruleset(name="%s"){
action(type="omfwd"
target="%s"
protocol="udp" port="%s"
)
}
input(type="imfile" ruleset="%s" tag="%s" file="%s")
	'''%(ruleset_name,ip,port,ruleset_name,tag,filepath)

	# content_text1='''module(load="imfile" )\nruleset(name="{rule_name}")'''.format(rule_name=ruleset_name)

	# content_text2='''action(type="omfwd" \ntarget="{ip}" \nprotocol="udp" port="{port}")'''.format(ip=ip,port=port)

	# content_text3=r'''input(type="imfile" ruleset="{rule_name}" tag="{tag}" file="{filepath}" )'''.format(tag=tag,rule_name=ruleset_name,filepath=filepath)
	# coentent=content_text1+r'{'+content_text2+'}\n'+content_text3
	# return coentent
	return ttt

def set_choice(choice_type,type_list,file_path,suffix_string):
	'''
	update the state
	'''
	type_list[choice_type]+=1

	for key in type_list:

		if type_list[choice_type]%2==0:
			'''del'''

			f=open(file_path,'r+')
			m=f.readlines()
			f.close()
			line1=r'#'+choice_type+r'.* '+suffix_string+'\n'
			line2=choice_type+r'.* '+suffix_string+'\n'

			n_line=m.index(line2)

			f=open(file_path,'w+')

			m[n_line]=line1
			f.writelines(m)
			f.close()
			# deal_read(file_path,choice_type,suffix_string,0)
			break
		else:
			'''add'''

			f=open(file_path,'r+')
			m=f.readlines()
			f.close()

			line1=r'#'+choice_type+r'.* '+suffix_string+'\n'
			line2=choice_type+r'.* '+suffix_string+'\n'

			# print line1,m
			n_line=m.index(line1)

			f=open(file_path,'w+')

			m[n_line]=line2
			f.writelines(m)
			f.close()
			# deal_read(file_path,choice_type,suffix_string,1)
			break
	f.close()

def print_on_of_dict(type_list):
	'''
	'''
	new_dict=dict(type_list)
	space_length=50
	item = sorted(new_dict.keys())
	print '|'+'--'*3+'---------'+'--'*3+'|'
	print '|'+'  '*3+'log state'+'  '*3+'|'

	print '|'+'-'*(space_length-2)+'|'
	for n,x in enumerate(item):
		if new_dict[x]%2==1:
			str1=str(n+1)+' '*4+x+':'+'on'
			if len(str1)<space_length:
				print_format_string(str1,space_length)
			# print str1
		else:
			str2=str(n+1)+' '*4+x+':'+'off'
			if len(str2)<space_length:
				print_format_string(str2,space_length)
			# print str2

	print '|'+' '*(space_length-2)+'|'

	add='a:'+' '*4+'add new type log'
	print_format_string(add,space_length)

	recover='r:'+' '*4+':recover origin conf file'
	print_format_string(recover,space_length)

	quit='q or 0:'+' '*4+':quit'
	print_format_string(quit,space_length)

	print '|'+'-'*(space_length-2)+'|'
	print '\n'

def print_format_string(input_str,space_length):
	xx='|'+input_str+' '*(space_length-len(input_str)-2)+'|'
	print xx
def print_title():
	'''
	'''

	print '###########################################'
	print '#          message info below             #'
	print '###########################################'
	print '\n'
	s=False
	input_id=''
	while not s:
		input_id= raw_input('input the WebUI key to identifies your log:\n ')

		if check_key(input_id):
			s=True
		else:
			print 'key format error!'
		if s:
			break
	return input_id

def check_key(stringkey):
	'''
	'''
	return [True,1]
def restart_service():
	'''
	restart rsyslog service
	'''
 	cmd=r'sudo service rsyslog restart'
 	ret=Popen(cmd,shell=True,stdout=PIPE)
 	t=ret.stdout.readlines()
 	for line in t:
 		if 'process' in line:
 			print 'rsyslog restart success'
 	'''
	to show on used log types
	'''
def show_on_log_type(content):
	''''''
	c=list(content)
	on_type=[]

	for line in c:
		if r'#' in line[1][0]:
			# print line[0],line[1]
			pass
		else:
			on_type.append(line)
	'''
	add code to show support type log

	'''
	return on_type

def bakup_conf(filename):
	'''
	first to check whether there exists bakup file ,if it exists,no operation,
	if not ,then make a bakup file of syslog conf
	'''
	print '------'
	if not os.path.isfile(filename+'.old'):
		target_path=r''
		cmd=r'cp '+filename+r' '+filename+r'.old'
		if call(cmd,shell=True)==0:
			'''after success add #type.*@remover_ip_port to the conf file '''
			type_list=['auth','cron','daemon','kern','lpr','mail','user','news']
			server_ip_port=r'192.168.70.104:514'
			suffix_string=r'@@'+server_ip_port
			#add $WorkDirectory /var/lib/rsyslog
			#add
			addline=r'$WorkDirectory /var/lib/rsyslog'
			# f.write(addline+'\n')
			try:
				f=open(filename,'a')
				# f.write('$ActionFileEnableSync on\n')
				for x in type_list:
					line=r'#'+x+r'.* '+suffix_string
					f.write(line+'\n')
				'''

				'''
				f.close()
			except:
				print 'add info fail!'
				return False
			return True
		else:
			print 'bakup file fail!'
			exit(1)
	else:
		# print 'no create .old file'
		'''secedn run time maybe write new log type'''
		# if argv:
		# 	print 'zuijia wenjian '
		# 	type_list=['auth','cron','daemon','kern','lpr','mail','user','news']
		# 	file_name=argv[0]

		# 	log_local_path=argv[1]
		# 	try:

		# 		f=open(filename,'a')
		# 		line=file_name+' '+log_local_path
		# 		f.write(line+'\n')
		# 		f.close()
		# 	except:
		# 		raise 'add new log type [%s] fail!'%(file_name)
		# else:
		# 	print 'bu zhuiji'

		return False

def check_script_argv(argv):
	if len(argv)==3:
		if r'/' not in sys.argv[2]:
			raise 'syntax error'
		else:
			return sys.argv[1:3]
	else:
		return False


def main():

	# argv=False
	# if len(sys.argv)==1:
	# 	pass
	# else:
	# 	argv=check_script_argv(sys.argv)

	# print argv


	server_ip=r'192.168.1.1'
	RSYSLOG_CONF_DIR=r'/etc/rsyslog.d'
	RSYSLOG_SERVICE=r'rsyslog'
	USER_KEY=''
	os_info=get_os()
	print os_info


	# osname=check_os(os_info)
	osname=os_info
	if check_privilege():
		pass
	else:
		raise 'root or sudo!'
	USER_KEY=print_title()
	if osname:
		if check_hostname():
			if check_privilege():
				if check_network(server_ip):
					if check_auto_rsyslog():
						if set_choice_rsyslog(osname,USER_KEY):
							restart_service()
							print 'success and bye bye\n'

						else:
							raise 'error set rsyslog conf'
					else:
						raise 'rsyslog is not auo server'
				else:
					raise 'not connect to server ip'
			else:
				raise 'not root,please use sudo or root account'
		else:
			raise 'can not find hostname!'
	else:
		raise 'can not find os info!'

if __name__=='__main__':
	main()
	# s={'ip':12,'tag':'21x3','ruleset':'haha','filepath':'/var','ruleset_name':'222','port':'3333'}
	# # print s['tag']
	# # print s['tag''{name},{age}'.format(age=18,name='kzc')]
	# # print '''132123{tag}'''.format(tag=s['tag'])
	# a=make_user_manual_conf(s)
	# print a


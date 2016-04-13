#!/bin/bash

#############################################
#
#	Logentries Agent Installer
#
#	Supported Distro's:
#		Debian 5 and newer
#		Ubuntu 12.04/14.04 and newer
#		CentOS/RedHat 6/7 newer
#
#############################################

VERSION="1.0.0"

# Need root to run this script
if [ "$(id -u)" != "0" ]
then
	echo "Please run this install script as root."
	echo "Usage: sudo bash loginsight_install.sh"
	exit 1
fi

# Fixme Add diff repo for install according to the system version

if  [ lsb_release -i |awk '{print $3}' = "Ubuntu" ]
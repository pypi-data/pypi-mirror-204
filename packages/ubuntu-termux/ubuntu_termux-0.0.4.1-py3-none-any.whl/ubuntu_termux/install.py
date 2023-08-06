
'''
Author: ReinanBr <slimchstuba@gmail.com>
dateInit: 15/10/2022 08:39
ProjectInfo: Ubuntu-Termux
About: lib for install ubuntu in termux with python
LICENSE: GPLv2
'''

import os
import sys
import kitano as kt
from kitano import puts
from kitano.termux import ShellRun
import os

commandInstall = '''pkg update && pkg upgrade -y
pkg install wget -y
pkg install proot -y
pkg install git -y
cd ~
git clone https://github.com/MFDGaming/ubuntu-in-termux.git
cd ubuntu-in-termux
chmod +x ubuntu.sh
./ubuntu.sh
cd ~
cd ..
echo 'cd ~ && cd ubuntu-in-termux && ./startubuntu.sh' > usr/bin/ubuntu
chmod +x usr/bin/ubuntu
ubuntu'''


sr = ShellRun()
sr.prt = True

#kt.show_date(True)

def install_ubuntu_termux():
	if 'android' in sr.checkLine('uname -a') and 'linux' in sr.checkLine('uname -a'):
		
		print('Yes! You is a Android with linux')
		#installing the libs base..
		os.chdir('/data/data/com.termux/files/home')
		if os.path.isdir('ubuntu-in-termux'):
			print('removing cache...')
			os.system('rm -rf ubuntu-in-termux')
			print('ok!')
		sr.runLine(commandInstall)
		

#install_ubuntu_termux()

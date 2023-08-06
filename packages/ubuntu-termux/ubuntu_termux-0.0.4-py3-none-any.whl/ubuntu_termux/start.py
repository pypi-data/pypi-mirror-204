from ubuntu_termux.install import install_ubuntu_termux as iut
import os,kitano as kt

kt.show_date(True)

def installNow():
	os.chdir('/data/data/com.termux/files')
	if not os.path.isfile('usr/bin/ubuntu'):
		print('ubuntu not found, installing...')
		iut()
	else:
		print('ubuntu is installed!\nrun with:\n->$ ubuntu')




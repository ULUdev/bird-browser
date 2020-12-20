#!/bin/bash
if [ $USER = "root" ]; then
		pip3 install bird-browser
		echo python3 -m bird-browser > /bin/bird-browser
		chmod 700 /bin/bird-browser
else
		echo file needs to be executed as root
		echo try 'sudo install.sh' instead
fi

#!/bin/bash
if [ "$1" = "install" ]; then
	if [ "$USER" = "root" ]; then
		pip3 install PyQt5
		pip3 install PyQtWebEngine
	else
		echo source as root sudo source setup.sh install
	fi
elif [ "$1" = "venv" ]; then
	python3 -m venv .
	source bin/activate
	pip3 install PyQt5
	pip3 install PyQtWebEngine
fi

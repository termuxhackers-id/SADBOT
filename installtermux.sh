#!/usr/bin/bash
pkg update -y
pkg upgrade -y
pkg install aapt python -y
pip3 install --upgrade pip
pip3 install pyshodan rich prompt_toolkit
pkg install wget -y
wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh

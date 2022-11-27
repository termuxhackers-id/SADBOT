#!/usr/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y aapt python3 python3-pip
sudo apt-get install -y android-tools-adb android-tools-fastboot
sudo pip install --upgrade pip
sudo pip install pyshodan rich prompt_toolkit

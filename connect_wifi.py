#!/usr/bin/env python
import os
import sys
from pyroute2 import IPRoute,IPBatch
import subprocess, signal
import csv
import time
import re
# -*- coding: utf-8 -*-
"""
Connect_Wifi.py v1.0

The script will connect you to your wifi even if you had problem with your network manager 

or wicd or even if you by mistake removed your network manager

you just need to gave the script your wifi interface name and your password 

(how this script work)

we will use airmon-ng to set wifi interface to monitor mode then we will use 

airodump-ng to scan for your wifi name if you dont know and print result

you will input the ESSID name (wifi name) 

wpa_passphrase will create a config file to use it in wpa_supplicant to connect to the wifi 

===== make sure to check the requirements.txt ======

use 
    1: (sudo apt-get install python-pip)

    2: (sudo pip install -r requirements.txt)

==== require aircrack ======

can be find in the downloaded package 

use 
    1: (tar zxf aircrack-ng-1.2-rc4.tar.gz)

    2: (cd aircrack-ng-1.2-rc4)

    3: (make)

    4: (sudo make install)


Created By XxoraxX 


"""
# ----- Run The Script As Root -----
if os.geteuid() !=0:
	os.execvp("sudo", ["sudo"] + sys.argv)

ip   = IPRoute()
ipb  = IPBatch()
mode = [x.get_attr('IFLA_IFNAME') for x in ip.get_links()]

# ------ send a command to the shell and return the result --------
def cmd(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
).stdout.read().decode()

# --------subprocess to kill wpa_supplicant if runing  -------------
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)

out, err = p.communicate()

for line in out.splitlines():

	if 'wpa_supplicant' in line:

		pid = int(line.split(None, 1)[0])

		os.kill(pid, signal.SIGKILL)

# --------subprocess to dhclient if runing kill -------------
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)

out, err = p.communicate()

for line in out.splitlines():

	if 'dhclient' in line:

		pid = int(line.split(None, 1)[0])

		os.kill(pid, signal.SIGKILL)

# ------ Print Local Interface Name -----

print([x.get_attr('IFLA_IFNAME') for x in ip.get_links()])

time.sleep(1)

# ----- nface name for the wifi interface --------
nface = raw_input("Please Chose Your Wifi Interface Name: ")

# --------pwifi password for the wifi router -------
pwifi = raw_input("Please Input Your Wifi Password: ")

print("Check If Your Wifi Interface In Monitor Mode") 

time.sleep(1)

# -------idx put interface in up mode---------- 
idx = ip.link_lookup(ifname=(nface))[0]

ipb.link("set", index=idx, state="up")

# ---------subprocess to call airmon-ng -----------
def mmode(x,z):
	if x in mode:
		print("Your Interface In Monitor Mode")
	elif z in mode:
		print("Your Interface In Monitor Mode")
	else:
		x in mode
		print("Puting Your Interface In Monitor Mode")
		subprocess.call(['airmon-ng', 'start', (nface)])
mmode('mon0','wlan0mon')

#  -------------os.system to open new terminal and call airodump wait for 8 sec then close ---------
amode = [x.get_attr('IFLA_IFNAME') for x in ip.get_links()]
def dmode(x,z):
	if x in amode:
		os.system("gnome-terminal -e 'bash -c \"airodump-ng mon0 -w /tmp/airout ; exec bash\"', echo $$ ")
		time.sleep(8)
	elif z in amode:
		os.system("gnome-terminal -e 'bash -c \"airodump-ng wlan0mon -w /tmp/airout ; exec bash\"', echo $$ ")
		time.sleep(8)
dmode("mon0","wlan0mon")

	# --------subprocess to kill airodump-ng if runing -----------

p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)

out, err = p.communicate()

for line in out.splitlines():

	if 'airodump-ng' in line:

		pid = int(line.split(None, 1)[0])

		os.kill(pid, signal.SIGKILL)

# -------- Reading From CSV file -----------

def csv2blob(filename):

    with open(filename,'rb') as f:
        z = f.read()

    # Split into two parts: stations (APs) and clients

    parts = z.split('\r\n\r\n')
    
    stations = parts[0]
    
    clients = parts[1]

    import sys
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO

    stations_str = StringIO(stations)
    clients_str  = StringIO(clients)

    r = csv.reader(stations_str)
    i = list(r)
    z = [k for k in i if k <> []]

    stations_list = z

    r = csv.reader(clients_str)
    i = list(r)
    z = [k for k in i if k <> []]

    clients_list = z
    
    return stations_list, clients_list

csvfile='/tmp/airout-01.csv'

stations_list, clients_list = csv2blob(csvfile)


#################################
# Data for 
# Stations 
# (Access Points)
#################################

nstations = len(stations_list)

sthead = stations_list[0]

stations_head = [j.strip() for j in sthead]

stations_data = [stations_list[i] for i in range(1,nstations)]

for i,row in enumerate(stations_data):

    # get indices
    ap_mac_ix  = stations_head.index('BSSID')
    ap_name_ix = stations_head.index('ESSID')
    ap_sec_ix  = stations_head.index('Privacy')
    ap_pow_ix  = stations_head.index('Power')
    ap_ch_ix   = stations_head.index('channel')

    # get values
    ap_mac = row[ap_mac_ix].strip()
    ap_name = row[ap_name_ix].strip()
    ap_sec = row[ap_sec_ix].strip()
    ap_pow = row[ap_pow_ix].strip()
    ap_ch = row[ap_ch_ix].strip()

    if ap_name=='':
        ap_name="unlabeled"

    mac_name = re.sub('\:','_',ap_mac)

    ######################
    # Print out some information
    print "="*40
    print "ESSID:",ap_name
    print "Channel:",ap_ch
    print "MAC:",ap_mac
    print "Encryption:",ap_sec
    print "Power:",ap_pow
    print ""
# -------essid name for the wifi router -----------
essid = raw_input("Please Enter Your ESSID: ")

# ------- subprocess to call airmon to stop mon0 -----------

time.sleep(2)
mmode = [x.get_attr('IFLA_IFNAME') for x in ip.get_links()]
def rmode(x,z):
	if x in mmode:
		print("Puting Interface In Managed Mode")
		subprocess.call(['airmon-ng', 'stop', x ])
	elif z in mmode:
		print("Puting Interface In Managed Mode")
		subprocess.call(['airmon-ng', 'stop', z ])
	else:
		print("Done")
rmode("mon0","wlan0mon")

	
print ('Plese Wait We Are Trying To Connect You To Your Wifi Need 10 Sec')

time.sleep(2)

# -------- open a file and write output -------------		

with open('wpa.conf', 'w') as f:

    subprocess.call(['wpa_passphrase',(essid), (pwifi)], stdout=f)

# -------- subprocess to call wpa_supplicant and connect to wifi -------------------
subprocess.call(['wpa_supplicant', '-i', nface, '-c' 'wpa.conf', '-D' 'wext' ,'-B'])


# ---------subprocess to call dhclient and gave ip to interface --------------
subprocess.call(['dhclient', nface])

# -------- Remove Tmp file -------------
cmd("rm -R /tmp/")

cmd("mkdir /tmp/")

print("You Are Contect To Your Wifi")
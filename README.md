Connect Wifi V1.0

Connect Wifi V1.0 is a tool will connect you to your wifi even if you had problem with your network manager 

or wicd or even if you by mistake removed your network manager

you just need to gave the Tool your wifi interface name and your password 

How This Tool Work

It will use airmon-ng to set wifi interface to monitor mode then use 

airodump-ng to scan for your wifi name if you dont know and print result

you will input the ESSID name (wifi name) 

wpa_passphrase will create a config file to use it in wpa_supplicant to connect to the wifi .

===== Make Sure To Check The Requirements.txt ======

Use 
    
    1: ( sudo apt-get install python-pip )

    2: ( sudo pip install -r requirements.txt )

==== Require Aircrack ======

can be find in the downloaded package 

Use 

    1: ( tar zxf aircrack-ng-1.2-rc4.tar.gz ) 

    2: ( cd aircrack-ng-1.2-rc4 )

    3: ( make )

    4: ( sudo make install )

==========================================

Installation

Use 

      1: ( sudo chmod 775 connect_wifi.py )
   
      2: ( ./connect_wifi.py ) 


Tested on Ubuntu 16.04

Should Work On Kali 

Created By XxoraxX 

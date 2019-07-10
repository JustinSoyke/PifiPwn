Bachelor of Information Technology (Network Security) - Meadowbank Tafe
Raspberry Pi Wireless Project - Stage 1


+==================+
| PifiPwn + PifiAP |
|  Version: 0.1    |
|  Justin Soyke    |
+==================+

Raspberry Pi Individual Project, It "should" work on any Linux device, just ensure you have dependencies installed.

Note: As this was a project for a subject, there's a high chance I won't maintain it, fix bugs, etc. Issues & Pull requests are welcome.  



+++ PifiPwn Features +++

- Start/Stop Monitor Mode
- Capture WPA Handshakes
- Send DeAuth Packets to AP Clients
- Crack WPA Handshake (Aircrack-ng)


+++ PifiAP Features +++

- Start/Stop Access Point
- View Connected Clients
- Routable to Networks via eth0 (Note: Make sure you use dhclient to get an IP from DHCP)

+++ Dependencies +++
PyQt5
Aircrack, Airodump, Airmon, Aireplay

--PifiPwn --
=== iwlist ===
https://github.com/iancoleman/python-iwlist
- Parses 'iwlist Interface scanning' to a nice output easily used.

-- PifiAP --
=== create_ap ===
https://github.com/oblique/create_ap
- For simplicity, I decided to use create_ap, the same AP Creation can easily
  be done using the usual methods, It simply just creates the configuration files
  and runs the required programs. (dnsmasq, hostapd, etc)
  Configuration can be set in the global configuration section below.


Demo:

![PifiPwn Demo](demo/PifiPwn-Demo.gif)



How to:
PifiPwn -

1. Make sure MonitorMode is Disabled (So we can actually scan, it is possible to use a different interface card,
   but you may run into issues.

2. Click "Scan APs", It'll bring up a list of Access Point's ESSID in range

3. Click on the Access Point Name (Note: Ensure that you click the correct Access Point  as it uses the data retrieved
   from iwlist for the rest of the program)

4. Click "Start Mon0"  to put the Interface into Monitor Mode.

5. Click on "Capture Handshakes, almost immediately click on Send Deauth Packets by default configuration,
   each will only run Airodump-ng & Aireplay for 10 seconds to increase this time, simply change the configuration options below.

6. If a Handshake is captured, It will display that it's been captured in the output

7. After the Handshake has been captured, click on "Crack WPA Password", it'll crack the password via a Dictionary Attack.
   This can take some time on the Raspberry Pi, make sure to use a short 5-10k Wordlist.
   After the password has been cracked, It will display the password in the output section.

----

PifiAP

Simply click on Start AP, you can see the connected clients if you click on the refresh button
 (Note: If using the Interface as you're using for the PifiPwn, ensure that Monitor Mode
  is disabled before trying to start the AP.)
  Unless you setup dhclient to run on boot, eth0 will not get an IP Address without using the dhclient command.

----

Bugs:

- There's several bugs, due to using multiple ways to execute programs (subprocess & QProcess)

- Some of the buttons freeze up the UI until it has finished executing (Which is great for Start/StopAP, Start/StopMon)
- Clicking buttons multiple times may cause programs being executed multiple times, hence causing unstability, potentially
  causing Interfaces to screw up, could also cause the app to crash.
- When cracking a password, It may not always spit out the cracking progress, occasionally it'll output random lines
  and the current password being cracked, this is due to the lines not always being the same size in stdout,
  it's about 50/50 that it'll output correctly.

- Output Colours appear to be different on the Raspberry Pi, compared to a standard Linux machine

To-do:

- Clean up code
- Fix bugs
- Restructure and move calls to QProcess instead of Subprocess
- Add other Wireless Attack Features, such as WPS,  WEP,  RogueAP, etc
- Re-do the output regex, to only send the right cracking status - Probably just re.sub everything but what we want

To-do Features:

- Implement Bluetooth related tools
- Implement RogueAP
- Implement additional wireless/portable penetration testing/exploitation functions. ;)


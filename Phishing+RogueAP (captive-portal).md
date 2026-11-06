
If we try to perform the same attacks as with the previous networks we can see that it is not possible, since as we have seen in the section on EAP methods, the AP only supports client certificate access.

So we cannot attack this network, but we can attack its clients, because as we can see in the Probes, there is a client of this network that asks for the following networks “open-wifi,home-WiFi,WiFi-Restaurant”. So we can create an AP with that name, deauthenticate the wifi-global client and perform a phishing attack with a captive portal to obtain its credentials. For this we can use “eaphammer” with “—captive-portal” and perform the deauthentication attack with “aireplay-ng”.


**Phishing+RogueAP (captive-portal)**

If we try to perform the same attacks as with the previous networks we can see that it is not possible, since as we have seen in the section on EAP methods, the AP only supports client certificate access.

So we cannot attack this network, but we can attack its clients, because as we can see in the Probes, there is a client of this network that asks for the following networks “open-wifi,home-WiFi,WiFi-Restaurant”.


```
sudo killall dnsmasq
sudo eaphammer --essid WiFi-Restaurant --interface wlan4 --captive-portal
```


```
iwconfig wlan0mon channel 44
aireplay-ng -0 0 wlan0mon -a F0:9F:C2:71:22:17 -c 64:32:A8:BC:53:51
```

```
hashcat -m 5600 hash -a 0 /root/rockyou-top100000.txt
```
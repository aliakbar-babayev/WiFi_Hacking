
Wireless interfaces are a cornerstone of wi-fi penetration testing. After all, our machines transmit and receive this data through these interfaces. If we didn't have them, we could not communicate. We must consider many different aspects when choosing the right interface. If we choose too weak of an interface, we might not be able to capture data during our penetration testing efforts. In this section, we will explore all of the things we should consider when purchasing an interface for wi-fi penetration testing.


Of course, this output can be lengthy, but all the information in here is pertinent to our testing efforts. From the above example, we know that this interface supports the following.

1. `Almost all pertinent regular ciphers`
2. `Both 2.4Ghz and 5Ghz bands`
3. `Mesh networks and IBSS capabilities`
4. `P2P peering`
5. `SAE aka WPA3 authentication`



#### Scanning Available WiFi Networks

To efficiently scan for available WiFi networks, we can use the `iwlist` command along with the specific interface name. Given the potentially extensive output of this command, it is beneficial to filter the results to show only the most relevant information. This can be achieved by piping the output through grep to include only lines containing `Cell`, `Quality`, `ESSID`, or `IEEE`.

```
babayevvvv@htb[/htb]$ iwlist wlan0 scan |  grep 'Cell\|Quality\|ESSID\|IEEE'

          Cell 01 - Address: f0:28:c8:d9:9c:6e
                    Quality=61/70  Signal level=-49 dBm  
                    ESSID:"HTB-Wireless"
                    IE: IEEE 802.11i/WPA2 Version 1
          Cell 02 - Address: 3a:c4:6e:40:09:76
                    Quality=70/70  Signal level=-30 dBm  
                    ESSID:"CyberCorp"
                    IE: IEEE 802.11i/WPA2 Version 1
          Cell 03 - Address: 48:32:c7:a0:aa:6d
                    Quality=70/70  Signal level=-30 dBm  
                    ESSID:"HackTheBox"
                    IE: IEEE 802.11i/WPA2 Version 1
```



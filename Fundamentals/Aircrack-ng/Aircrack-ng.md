
Aircrack-ng is a powerful tool designed for network security testing, capable of cracking WEP and WPA/WPA2 networks that use pre-shared keys or PMKID. Aircrack-ng is an offline attack tool, as it works with captured packets and doesn't need direct interaction with any Wi-Fi device.

### Cracking WEP

Aircrack-ng is capable of recovering the WEP key once a sufficient number of encrypted packets have been captured using Airodump-ng. It is possible to save only the captured IVs (Initialization Vectors) using the `--ivs` option in Airodump-ng. Once enough IVs are captured, we can utilize the `-K` option in Aircrack-ng, which invokes the Korek WEP cracking method to crack the WEP key.

```
 aircrack-ng -K HTB.ivs 
```

### Cracking WPA

Aircrack-ng has the capability to crack the WPA key once a "four-way handshake" has been captured using Airodump-ng. To crack WPA/WPA2 pre-shared keys, only a dictionary-based method can be employed, which necessitates the use of a wordlist containing potential passwords. A "four-way handshake" serves as the required input. For WPA handshakes, a complete handshake comprises four packets. However, Aircrack-ng can effectively operate with just two packets. Specifically, EAPOL packets 2 and 3, or packets 3 and 4, are considered a full handshake.

```
aircrack-ng HTB.pcap -w /opt/wordlist.txt
```


 
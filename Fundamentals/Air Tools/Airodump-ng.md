

Airodump-ng serves as a tool for capturing packets, specifically targeting raw 802.11 frames. Its primary function lies in the collection of WEP IVs (Initialization Vectors) or WPA/WPA2 handshakes, which are subsequently utilized with aircrack-ng for security assessment purposes.

Furthermore, airodump-ng generates multiple files containing comprehensive information regarding all identified access points and clients. These files can be harnessed for scripting purposes or the development of personalized tools.

`airodump-ng` provides a wealth of information when scanning for WiFi networks. The table below explains each field along with its description:

|**Field**|**Description**|
|---|---|
|`BSSID`|Shows the MAC address of the access points|
|`PWR`|Shows the "power" of the network. The higher the number, the better the signal strength.|
|`Beacons`|Shows the number of announcement packets sent by the network.|
|`#Data`|Shows the number of captured data packets.|
|`#/s`|Shows the number of data packets captured in the past ten seconds.|
|`CH`|Shows the "Channel" the network runs on.|
|`MB`|Shows the maximum speed supported by the network.|
|`ENC`|Shows the encryption method used by the network.|
|`CIPHER`|Shows the cipher used by the network.|
|`AUTH`|Shows the authentication used by the network.|
|`ESSID`|Shows the name of the network.|
|`STATION`|Shows the MAC address of the client connected to the network.|
|`RATE`|Shows the data transfer rate between the client and the access point.|
|`LOST`|Shows the number of data packets lost.|
|`Packets`|Shows the number of data packets sent by the client.|
|`Notes`|Shows additional information about the client, such as captured EAPOL or PMKID.|
|`PROBES`|Shows the list of networks the client is probing for.|
Once Monitor mode is enabled, we can run `airodump-ng` by specifying the name of the targeted wireless interface, such as `airodump-ng wlan0mon`. This command prompts airodump-ng to start scanning and collecting data on the wireless access points detectable by the specified interface.


```
sudo airodump-ng wlan0mon
```

### Scanning Specific Channels or a Single Channel

The command `airodump-ng wlan0mon` initiates a comprehensive scan, collecting data on wireless access points across all the `channels` available. However, we can specify a particular channel using the `-c` option to focus the scan on a specific frequency. For instance, `-c 11` would narrow the scan to `channel 11`. This targeted approach can provide more refined results, especially in crowded Wi-Fi environments. Selecting the same channel as the AP's will allow us not to miss any packets. `airodump-ng`, while scanning, will hop between multiple channels, which is called `channel hopping`, allowing us to obtain as much information as possible about the surrounding environment.

```
sudo airodump-ng -c 11 wlan0mon
```


### Saving the output to a file

We can preserve the outcomes of our `airodump-ng` scan by utilizing the `--write <prefix>` parameter. This action generates multiple files with the specified prefix filename. For instance, executing `airodump-ng wlan0mon --write HTB` will generate the following files in the current directory.

- HTB-01.cap
- HTB-01.csv
- HTB-01.kismet.csv
- HTB-01.kismet.netxml
- HTB-01.log.csv

```
sudo airodump-ng wlan0mon -w HTB
```



The classic [ARP Request Replay Attack](https://www.aircrack-ng.org/doku.php?id=arp-request_reinjection) is a highly effective and reliable method for generating new initialization vectors (IVs). In this attack, an ARP packet is captured and retransmitted back to the access point (AP). This action prompts the AP to resend the packet, but with a new IV each time. The continuous replay of the same ARP packet forces the AP to respond repeatedly with different IVs. Collecting these packets with new IVs allows for the eventual determination of the WEP key.

To conduct an ARP Request Replay attack, `aireplay-ng` will be used to capture a valid ARP request, which is then replayed continuously until enough initialization vectors are gathered to crack the key (using either the `Korek/FMS` attack or the default `PTW` attack).

---


We first need to enable monitor mode on our wireless network interface. This allows us to capture and inject packets.

```
sudo airmon-ng start wlan0
```

We can test to see if our interface is in monitor mode with the `iwconfig` utility.

#### Performing the Attack

To begin, we scan our target access point using `airodump-ng` and capture the communication into a file. We specify our interface in monitor mode with `wlan0mon`, the channel our access point is running on with `-c`, and the name/path of our capture file with the `-w` argument.

```
airodump-ng wlan0mon -c 1 -w WEP
```

The above command will continuously scan the target access point and capture the communication, saving it into a file named `WEP-01.cap`. If there were multiple access points (APs) available and we wanted to focus on one specifically, we would use the `-b` option followed by the BSSID of the target AP.

In a second terminal, we can launch the ARP request replay attack using `aireplay-ng`. We specify the ARP request replay attack mode with `-3`, the BSSID of the target AP with `-b`, and the client MAC address with `-h`. Once a valid ARP request is captured, the tool will replay it automatically.

```
sudo aireplay-ng -3 -b B2:D1:AC:E1:21:D1 -h 4A:DD:C6:71:5A:3B wlan0mon
```


Initially, the number of captured ARP requests will be zero. When a valid ARP request is captured, it will be replayed multiple times, causing the number of captured ARP requests to increase rapidly.

Once we have generated enough ARP traffic, we can attempt to crack the key with `aircrack-ng`. We supply the `-b` option followed by our target BSSID, along with the `WEP-01.cap` file, where all the initialization vectors are stored.

```
aircrack-ng -b B2:D1:AC:E1:21:D1 WEP-01.cap
```





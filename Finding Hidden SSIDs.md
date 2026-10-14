
In WiFi networks, the Service Set Identifier (SSID) is the name that identifies a particular wireless network. While most networks broadcast their SSIDs to make it easy for devices to connect, some networks choose to hide their SSIDs as a security measure. The idea behind hiding an SSID is to make the network less visible to casual users and potential attackers. However, this method only provides a superficial layer of security, as determined attackers can still discover hidden SSIDs using various techniques.


#### Watching the Hidden Network

First, we need to set our interface to monitor mode.

```
sudo airmon-ng start wlan0
```


#### Scanning WiFi Networks

We can use `airodump-ng` to scan for available wifi networks.

```
sudo airodump-ng -c 1 wlan0mon
```


From the above output, we can see that there are three hidden SSIDs. The `<length: x>` notation indicates the length of the WiFi network name, where x represents the number of characters in the SSID.


There are multiple ways to discover the name of a hidden SSID. If there are clients connected to the WiFi network, we can use `aireplay-ng` to send deauthentication requests to the client. When the client reconnects to the hidden SSID, `airodump-ng` will capture the request and reveal the SSID. However, deauthentication attacks do not work on [WPA3](https://github.com/aircrack-ng/aircrack-ng/issues/2539) networks since WPA3 has 802.11w (Protected Management Frames, [PMF](https://www.wi-fi.org/beacon/philipp-ebbecke/protected-management-frames-enhance-wi-fi-network-security)) which authenticates the deauthentication. In such cases, we can attempt a brute-force attack to determine the SSID name.


### Detecting Hidden SSID using Deauth

The first way to find a hidden SSID is to perform a deauthentication attack on the clients connected to the WiFi network, which allows us to capture the request when they reconnect. From the above `airodump-ng` scan, we observed that a client with the STATION ID `02:00:00:00:02:00` is connected to the BSSID `B2:C1:3D:3B:2B:A1`. Let's start the `airodump-ng` capture on channel `1` and use `aireplay-ng` to send deauthentication requests to the client.


```
sudo airodump-ng -c 1 wlan0mon
```

In order to force the client to send a probe request, it needs to be disconnected. We can do this with aireplay-ng.

```
sudo aireplay-ng -0 10 -a B2:C1:3D:3B:2B:A1 -c 02:00:00:00:02:00 wlan0mon
```

After sending the deauthentication requests using `aireplay-ng`, we should see the name of the hidden SSID appear in `airodump-ng` once the client reconnects to the WiFi network. This process leverages the re-association request, which contains the SSID name, and allows us to capture and identify the hidden SSID.

```
sudo airodump-ng -c 1 wlan0mon
```



### Bruteforcing Hidden SSID

Another way to discover a hidden SSID is to perform a brute-force attack. We can use a tool like [mdk3](https://github.com/charlesxsh/mdk3-master) to carry out this attack. With mdk3, we can either provide a wordlist or specify the length of the SSID so the tool can automatically generate potential SSID names.


```
mdk3 <interface> <test mode> [test_ options]
```

|**Option**|**Description**|
|---|---|
|`-e`|Specify the SSID for probing.|
|`-f`|Read lines from a file for brute-forcing hidden SSIDs.|
|`-t`|Set the MAC address of the target AP.|
|`-s`|Set the speed (Default: unlimited, in Bruteforce mode: 300).|
|`-b`|Use full brute-force mode (recommended for short SSIDs only). This switch is used to show its help screen|

```
sudo mdk3 wlan0mon p -b u -c 1 -t A2:FF:31:2C:B1:C4
```

#### Bruteforcing using a Wordlist

To bruteforce using a wordlist we can use `-f` as the `test_option` in mdk3 followed by the location of the wordlist.

```
sudo mdk3 wlan0mon p -f /opt/wordlist.txt -t D2:A3:32:13:29:D5
```



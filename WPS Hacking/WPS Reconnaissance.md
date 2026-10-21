
In order to analyze a target network, we need to view its WPS information. We can do so with several different tools. Some of the information we hope to attain is the MAC address of the access point and which WPS version it is using. The MAC address is useful because an easy vendor lookup may allow us to find that the access point's vendor may or may not be susceptible to different kinds of WPS attacks. This can easily be done with a bit of research, and later we will explore custom PIN generation based on this information. Additionally, we want to find which version of WPS is running, along with which mode it is in, as it will help us narrow down which attack techniques to employ. If an access point is running WPS version 2.0 it is unlikely that we will be able to use any vector beyond pixie dust attacks, possibly null pin attacks, and brute forcing attempts with very long reattempt periods. This is due to a few factors, such as a locking feature built into most access points. After a certain amount of incorrectly guessed PINs the access point locks and requires either a reboot or timeout for additional PIN guesses.


### Scanning WPS Networks with Airodump-ng

```
airmon-ng start wlan0
```


```
airodump-ng --wps --ignore-negative-one wlan0mon
```


```
airodump-ng --wps --ignore-negative-one -c 8 --bssid 60:38:E0:XX:XX:XX wlan0mon
```

With Airodump-ng, we can obtain solid information about the WPS version and the mode it is using to operate. WPS includes several different modes, and Airodump-ng uses the following acronyms to represent them.

|Acronym|Description|
|---|---|
|`DISP`|The Access Point generates a PIN in its administrative setup portal, and the PIN can be found there.|
|`ETHER`|A rare mode that allows enrollees and registrars to undergo setup over Ethernet.|
|`EXTNFC`|WPS using Near Field Communication.|
|`INTNFC`|WPS using Near Field Communication.|
|`KPAD`|Keypad PIN method configuration. Enrollees connect by entering the WPS PIN into a keypad on the client device.|
|`LAB`|The PIN is displayed on a label attached to the access point itself.|
|`Locked`|WPS is locked. This can occur from too many incorrect guesses.|
|`NFCINTF`|WPS using Near Field Communication.|
|`PBC`|Push Button Configuration. Allows clients to join by pressing the WPS button on both the access point and the client device.|
|`USB`|Data is transferred between the access point and the client through a USB interface.|

### Scanning WPS Networks with Wash

Wash is another great tool for scanning networks with WPS. We can employ a simple command with wash to display all networks with WPS and their respective versions.

```
wash -i wlan0mon
```

It is important to check the `wps_locked` status from wash. If it is set to 2, it means WPS is not in a locked state. Additionally, we can find out which vendor is associated with the access point with the following command, specifying the beginning of the MAC address.

```
grep -i "84-1B-5E" /var/lib/ieee-data/oui.txt
```


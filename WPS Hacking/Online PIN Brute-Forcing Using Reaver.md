
[Reaver](https://github.com/t6x/reaver-wps-fork-t6x) is an excellent tool for conducting online password cracking attempts. It offers various options, including Null PIN attacks, custom PIN associations, Pixie Dust Attacks, and general brute-forcing. We will explore Pixie Dust Attacks in detail in the later section. In this section, we will focus on brute-forcing WPS PINs using reaver.

### Reaver Usage

```
reaver -i [interface] -b [BSSID] -c [channel]
```

|**Option**|**Description**|
|---|---|
|`-i`|Name of the monitor-mode interface to use|
|`-b`|BSSID of the target AP|
|`-c`|Set the 802.11 channel for the interface|
|`-p`|Use the specified pin|
|`-d`|Set the delay between pin attempts|
|`-l`|Set the time to wait if the AP locks WPS pin attempts|
|`-g`|Quit after num pin attempts|
|`-r`|Sleep for y seconds every x pin attempts|
|`-t`|Set the receive timeout period|
|`-L`|Ignore locked state reported by the target AP|
|`-K, -Z`|Run pixiedust attack|
|`-O`|Write packets of interest into pcap file|

### Brute-forcing WPS PIN

To begin, we need to enable monitor mode. We can use the `iw` command to add a new interface named `mon0` and set its type to monitor mode, as demonstrated below. Due to a known bug, setting the interface to monitor mode using `airmon-ng` can cause `Reaver` to malfunction. Therefore, it is recommended to use the `iw` command for this purpose.

```
iw dev wlan0 interface add mon0 type monitor
```

```
ifconfig mon0 up
```

Once we've added an interface with monitor mode enabled, we can use `airodump-ng` to enumerate WPS enabled WiFi networks.

```
airodump-ng mon0 --wps
```


Now we can start bruteforcing using Reaver. To begin, we need to specify the interface with the `-i` argument, the BSSID with the `-b` argument, and the channel with the `-c` argument. Reaver will then automatically begin bruteforcing every possible PIN, which totals `11,000` possible PINs.

```
reaver -i mon0 -b AE:EB:B0:11:A0:1E -c 1 
```


### Bruteforcing using half known WPS PIN

If we know the first four digits of the WPS PIN, we can use Reaver to bruteforce the remaining four digits. We can provide the known half PIN using the `-p` option followed by the first four digits. For example, if the known first half of the PIN is 1234, we would use `-p 1234`.

```
reaver -i mon0 -b B2:A5:1D:E1:B2:11 -c 1 -p 1234
```


### Testing for Null PIN

Suppose neither of these succeed, we could also attempt a `Null PIN` attack. Some access points are vulnerable to Null PIN attacks and will even disclose the WPA-PSK when no PIN is sent. We can do so by employing the following command, specifying the Null PIN with `-p ""` or `-p " "`.

```
reaver -b 5A:1A:59:B7:E7:97 -c 1 -i mon0 -p " "
```


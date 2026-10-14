
Monitor mode is a specialized mode for wireless network interfaces, enabling them to capture all traffic within a WiFi range. Unlike managed mode, where an interface only processes frames addressed to it, monitor mode allows the interface to capture every packet of data it detects, regardless of its intended recipient. This capability is invaluable for network analysis, troubleshooting, and security assessments, as it provides a comprehensive view of the network's activity. By enabling monitor mode, users can intercept and analyze packets, detect unauthorized devices, identify network vulnerabilities, and gather comprehensive data on wireless networks. This mode provides a deeper level of insight into the wireless environment, facilitating more effective troubleshooting, security assessments, and performance evaluations.


We can set the wlan0 interface into monitor mode using the command `airmon-ng start wlan0`.

```
sudo airmon-ng start wlan0
```

We could test to see if our interface is in monitor mode with the iwconfig utility.

```
iwconfig
```


### Starting monitor mode on a specific channel

It is also possible to set the wireless card to a specific channel using `airmon-ng`. We can specify the desired channel while enabling monitor mode on the wlan0 interface.

```
sudo airmon-ng start wlan0 11
```



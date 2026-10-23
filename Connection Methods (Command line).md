
### WEP 

```
iwconfig wlan0 key 11:BB:33:CD:55
iwconfig wlan0 essid "TargetNetworkName"
ifconfig wlan0 up 
dhclient wlan0
```


### WPA 2

```
wpa_passphrase "wifi-mobile" "starwars1" > wifi-mobile.conf
```

```
sudo wpa_supplicant -B -i wlan0 -c wifi-mobile.conf
```

```
sudo dhclient wlan0
```

Bypassing MAC filtering in Wi-Fi networks is a technique used to circumvent a basic security measure that many wireless routers implement. MAC filtering involves allowing only devices with specific MAC (Media Access Control) addresses to connect to the network. While this adds a layer of security by restricting access to known devices, it is not foolproof. Skilled individuals can exploit weaknesses in this system to gain unauthorized access. This process typically involves MAC address spoofing, where an attacker changes their device's MAC address to match an allowed device, thereby gaining access to the network.


First, we would want to scout out our network with airodump-ng.

#### Scanning Available Wifi Networks

```
sudo airodump-ng wlan0mon
```


To bypass the MAC filtering, we can spoof our MAC address to match one of the connected clients. However, this approach often leads to collision events, as two devices with the same MAC address cannot coexist on the same network simultaneously.

A more effective method would be to either forcefully disconnect the legitimate client through deauthentication attacks, thereby freeing up the MAC address for use, or to wait for the client to disconnect naturally. This strategy is particularly effective in "bring your own device" (BYOD) networks, where devices frequently connect and disconnect.

#### Scanning Networks Running on 5Ghz Band

```
sudo airodump-ng wlan0mon --band a
```

From the above output, we can confirm that the ESSID `HTB-Wireless-5G` with the same BSSID is also operating on the `5 GHz` band. Since no clients are currently connected to the 5 GHz band, we can spoof our MAC address using tools such as [macchanger](https://github.com/alobbs/macchanger) to match one of the clients connected to the 2.4 GHz band and connect to the 5 GHz network without any collision events.

Before changing our MAC address, let's stop the monitor mode on our wireless interface.

```
sudo airmon-ng stop wlan0mon
```

```
sudo macchanger wlan0
```

As shown in the output, our Current MAC address and Permanent MAC address are `00:c0:ca:98:3e:e0`. Let's use `macchanger` to change our MAC address to match one of the clients connected to the 2.4 GHz network, specifically `3E:48:72:B7:62:2A`. This process involves disabling the `wlan0` interface, executing the `macchanger` command to adjust the MAC address, and finally reactivating the `wlan0` interface. Following these steps will effectively synchronize our device's MAC address with the specified client's address on the 2.4 GHz network.

```
sudo ifconfig wlan0 down
```

```
sudo macchanger wlan0 -m 3E:48:72:B7:62:2A
```

```
sudo ifconfig wlan0 up
```


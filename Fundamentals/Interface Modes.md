
There are many more pertinent modes we need to know for our wireless interfaces when we conduct wi-fi penetration testing. After all, each mode is responsible for different capabilities and roles when it comes down to the hierarchy of wi-fi communications. In this section, we will explore each of these separate modes, what they do, and how we can test our interface for their capabilities.

#### Managed Mode

Managed mode is when we want our interface to act as a client or a station. In other words, this mode allows us to authenticate and associate to an access point, basic service set, and others. In this mode, our card will actively search for nearby networks (APs) to which we can establish a connection.

Pretty much in most cases, our interface will default to this mode, but suppose we want to set our interface to this mode. This could be helpful after setting our interface into monitor mode. We would run the following command.

```
babayevvvv@htb[/htb]$ sudo ifconfig wlan0 down
babayevvvv@htb[/htb]$ sudo iwconfig wlan0 mode managed
```



#### Ad-hoc Mode

Secondarily, we could act in a decentralized approach. This is where ad-hoc mode comes into play. Essentially this mode is peer to peer and allows wireless interfaces to communicate directly to one another. This mode is commonly found in most residential mesh systems for their backhaul bands. That is their band that is utilized for AP-to-AP communications and range extension. However, it is important to note, that this mode is not extender mode, as in most cases that is actually two interfaces bridged together.

To set our interface into this mode, we would run the following commands.

```
babayevvvv@htb[/htb]$ sudo iwconfig wlan0 mode ad-hoc
babayevvvv@htb[/htb]$ sudo iwconfig wlan0 essid HTB-Mesh
```


#### Master Mode

On the flip side of managed mode is master mode (access point/router mode). However, we cannot simply set this with the `iwconfig` utility. Rather, we need what is referred to as a management daemon. This management daemon is responsible for responding to stations or clients connecting to our network. Commonly, in wi-fi penetration testing, we would utilize hostapd for this task. As such, we would first want to create a sample configuration.

```
babayevvvv@htb[/htb]$ nano open.conf

interface=wlan0
driver=nl80211
ssid=HTB-Hello-World
channel=2
hw_mode=g
```



#### Mesh Mode

Mesh mode is an interesting one in which we can set our interface to join a self-configuring and routing network. This mode is commonly used for business applications where there is a need for large coverage across a physical space. This mode turns our interface into a mesh point. We can provide additional configuration to make it functional, but generally speaking, we can see if it is possible by whether or not we are greeted with errors after running the following commands.

```
babayevvvv@htb[/htb]$ sudo iw dev wlan0 set type mesh
```


---

#### Monitor Mode

Monitor mode, also known as promiscuous mode, is a specialized operating mode for wireless network interfaces. In this mode, the network interface can capture all wireless traffic within its range, regardless of the intended recipient. Unlike normal operation, where the interface only captures packets addressed to it or broadcasted, monitor mode enables comprehensive network monitoring and analysis.

Enabling monitor mode typically requires administrative privileges and may vary depending on the operating system and wireless chipset used. Once enabled, monitor mode provides a powerful tool for understanding and managing wireless networks.


```
babayevvvv@htb[/htb]$ sudo ifconfig wlan0 down
```

```
babayevvvv@htb[/htb]$ sudo iw wlan0 set monitor control
```

```
babayevvvv@htb[/htb]$ sudo ifconfig wlan0 up
```


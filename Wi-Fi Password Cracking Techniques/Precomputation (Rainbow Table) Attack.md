
We can accelerate WPA-PSK cracking by performing a precomputation attack using [genpmk](https://github.com/joswr1ght/cowpatty/blob/master/genpmk.1). This tool generates a hash file by precomputing the Pairwise Master Keys (PMKs) from a given wordlist and the target Wi-Fi network's SSID. The resulting hash file can then be used with cowpatty to significantly speed up the cracking process, especially when the SSID is known in advance.

### Performing The Attack

We begin by enabling monitor mode on our `wlan0` interface using `airmon-ng`.

```
sudo airmon-ng start wlan0
```


Once our interface is in monitor mode, we use `airodump-ng` to scan for available Wi-Fi networks and their associated clients. Additionally, we use the option `-w WPA` to save the output of the scan into a file.

```
airodump-ng wlan0mon -c 1 -w WPA
```

We note the target SSID `HackTheBox`, then generate a precomputed PMK hash table for it using `genpmk`. The `-f` option specifies the wordlist, and `-d` defines the output file for the generated hashes.
```
aireplay-ng -0 5 -a 80:2D:BF:FE:13:83 -c 8A:00:A9:9B:ED:1A wlan0mon
```


```
genpmk -f /opt/rockyou.txt -d /tmp/hashtable -s HackTheBox
```


Once the handshake has been captured, we use `cowpatty` to match captured handshake against the generated hash table.

```
cowpatty -d hashtable -r WPA-01.cap -s HackTheBox
```

As shown in the output above, Cowpatty cracked the password in just `0.6 seconds`. Because the wordlist was precomputed for the target SSID, the cracking process was much faster. While precomputed attacks (rainbow tables) can greatly reduce cracking time, they come with a few drawbacks:

- `SSID-Specific Hashes`: Precomputed tables are only valid for a specific SSID. A unique table must be generated for each target network, making it inefficient for broad attacks.
- `Time-Consuming Generation`: Creating rainbow tables, especially for large wordlists, requires excessive amounts of time and computational resources.
- `High Storage Requirements`: The resulting tables can be quite large, especially when targeting multiple SSIDs or using extensive wordlists.

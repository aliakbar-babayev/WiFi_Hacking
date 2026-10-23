
In this section, we will walk through the process of capturing the 4-Way Handshake, which is essential for attacking WPA/WPA2-PSK networks. We'll start by verifying that the handshake capture is complete and usable. After that, we'll demonstrate how to recover the Pre-Shared Key (PSK) by cracking the handshake, giving you a clear understanding of how WPA/WPA2-PSK networks can be compromised. Finally, we'll connect to the network using the recovered key to show its practical use.

Keep in mind that the PMKID attack can sometimes bypass the need for a deauthentication step entirely. Still, the typical WPA/WPA2 workflow usually includes the following stages

1. `Reconnaissance`
2. `Handshake Capture`
3. `Password Cracking`
4. `Access Verification`

In some scenarios, we may choose not to perform cracking at all. Instead, we could use a hostile portal or evil twin attack to trick users into revealing their credentials directly. While this method can yield faster results, it is noisier and substantially more intrusive than capturing a PMKID or handshake and cracking it offline.

## 1. Reconnaissance

We begin by enabling monitor mode on our wlan0 interface using airmon-ng.

```
sudo airmon-ng start wlan0
```

Once our interface is in monitor mode, we can use airodump-ng to scan for available Wi-Fi networks and their associated clients. Additionally, we can use the option `-w WPA` to save the output of the scan into a file.

```
airodump-ng wlan0mon -c 1 -w WPA
```

## 2. Handshake Capture

The second step is to capture the 4-way handshake. This handshake occurs when a client connects to a WPA/WPA2-protected Wi-Fi network. By capturing this exchange, we obtain the necessary data to attempt password cracking offline.

![4-Way Handshake diagram: Client and Access Point exchange messages. Steps: Probe Request-Response, Authentication, Association; Message 1: Annonce; Message 2: Snonce + MIC; Message 3: Sends GTK + MIC; Message 4: Acknowledges Key installation. Pre-shared key: 256 bits.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/312/wpa_handshake/WPA_handshake.png)

By executing a deauthentication attack on connected clients using `aireplay-ng`, it forces them to reconnect to the access point. This allows us to capture the 4-way handshake using airodump-ng.


```
aireplay-ng -0 5 -a 80:2D:BF:FE:13:83 -c 8A:00:A9:9B:ED:1A wlan0mon
```


After initiating the deauthentication attack, the WPA handshake should appear in the `airodump-ng` output within a few seconds, indicating a successful capture.

```
airodump-ng wlan0mon -c 1 -w WPA
```


## 3. Password Cracking

We can now proceed with cracking the captured handshake in order to retrieve the pre-shared key (PSK). Several tools are available for cracking WPA handshakes, including John the Ripper, Hashcat, Cowpatty, and Aircrack-ng, among others. Let's examine each of these tools individually.

#### Using Cowpatty

[CowPatty](https://github.com/joswr1ght/cowpatty) is a tool commonly used to verify and crack WPA handshakes. To validate whether a proper handshake has been captured, we can use CowPatty in check mode with the `-c` flag, followed by the capture file using `-r`.

```
cowpatty -c -r WPA-01.cap
```


If a valid handshake is present, CowPatty will indicate so in the output. This confirms that the file can be used for cracking attempts. To crack a WPA-PSK handshake using CowPatty, we need to specify the capture file, the dictionary (wordlist) file, and the SSID of the target Wi-Fi network. The `-f` option specifies the wordlist, `-r` provides the path to the packet capture file, and `-s` defines the SSID:

```
cowpatty -r WPA-01.cap -f /opt/wordlist.txt -s HackTheBox
```

#### Using Aircrack-ng

We can also use [aircrack-ng](https://www.aircrack-ng.org/doku.php?id=aircrack-ng) to crack the WPA-PSK from a captured handshake file. This tool tests each password in the provided wordlist against the handshake to try and recover the correct pre-shared key (PSK). We can use `-w` to specify the path to the wordlist.

```
aircrack-ng WPA-01.cap -w /opt/wordlist.txt
```

#### Using John the Ripper

[John the Ripper](https://github.com/openwall/john) can also be used to recover WPA passphrases. However, since John requires a specific hash format, we must first extract and convert the necessary data from the `.cap` or `.pcap` file using [wpapcap2john](https://github.com/willstruggle/john/blob/master/wpapcap2john). This tool parses the captured 4-Way Handshake and generates a hash that John can use for offline password cracking.

```
wpapcap2john wpa-Induction.pcap
```

```
john hash --wordlist=/usr/share/wordlists/rockyou.txt --format=wpapsk
```

#### Using Hashcat

To crack WPA/WPA2 passwords with [Hashcat](https://hashcat.net/hashcat/), we first need to extract the appropriate hash from a `.pcap` or `.pcapng` capture file into Hashcat's accepted format. [hcxpcapngtool](https://github.com/ZerBea/hcxtools) is the go-to utility to convert handshake captures into Hashcat-friendly format.

```
hcxpcapngtool -o hash wpa-Induction.pcap
```

```
hashcat -m 22000 --force hash /opt/wordlist.txt
```


## 4. Access Verification

Once a valid PSK has been obtained (or valid credentials, in the case of WPA2-Enterprise), we can proceed with access verification. To do this, we simply enter the PSK or credentials into the system's network manager when prompted.

## Common Pitfalls

Cracking WPA or WPA2 handshakes can be highly time-consuming and in many cases unsuccessful. Whether the network type is WPA2 (offline cracking), WPA3 (online cracking), or WPA2-Enterprise (offline cracking), we may face several challenges during the process:

1. The actual password may not exist in our `wordlist`.
2. Brute-force attacks can take an impractical amount of time if we lack information about the `password structure`.
3. WPA/WPA2 passwords can range from `8` to `63` characters, depending on the implementation, making exhaustive searches difficult.
4. Passwords may be too `complex` or `unique` to appear in commonly used wordlists.
5. Default or commonly used password patterns may be `overlooked` during our attempts.

Regardless of the wireless standard we are targeting, it's important to ask ourselves a few key questions to improve our chances of success:

1. `Is the target network using WPA-Enterprise?` If so, we may be able to gather information about specific users, which can help us craft more effective, personalized wordlists.
2. `Do we know anything about the administrator?` Personal connections or online presence might reveal hobbies or interests that could influence password choices.
3. `Does the SSID indicate a default configuration?` If yes, we can attempt default password wordlists or create a custom list based on the device model or manufacturer.
4. `Do we have the computational resources to perform brute-force attacks?` If resources permit, we could consider incremental brute-force or hybrid attacks as a last resort.




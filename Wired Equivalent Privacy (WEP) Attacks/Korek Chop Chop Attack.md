
Not all access points (APs) are equal. During an assessment, we may find some are more vulnerable to fragmentation than others. As an alternative, we can employ the [Korek Chop Chop Attack](https://www.aircrack-ng.org/doku.php?id=korek_chopchop) to similarly capture a packet and retrieve the 1500 bytes of PRGA. Known technically as an `Inverse Arbaugh` attack, chop chop uses inductive reasoning to decrypt the packet without needing the key.

This is achieved by abusing the Integrity Check Value (ICV) in WEP. If we recall, the ICV ensures the integrity of the transmitted message. In the case of WEP, the CRC32 algorithm is used to calculate this value; if the ICV of a packet is not valid, it will be dropped by the access point (AP) upon receipt. This seemingly benign interaction creates an opportunity for attackers.

The attack works like this: after capturing a legitimate packet, the last byte of the encrypted message is removed and assigned a value (from 0-255) that we guess, starting at zero. A series of [calculations](https://www.aircrack-ng.org/doku.php?id=chopchoptheory) is performed to determine the ICV of the truncated packet, which has a mathematical relationship to the value of the missing byte. This new packet is sent into the network as we await the AP's response. If the packet is dropped, we guess a different number and try again. If the packet isn't dropped, it means our guess was correct, thus revealing the true value of the byte. We then "chop off" the next byte and repeat the process. As the packet is decrypted byte by byte, we are able to recover the PRGA simultaneously.

With the resulting keystream data (.xor file), we are able to craft and encrypt packets that look legitimate within the network. This allows us to subsequently perform the ARP request replay attack.

#### Enabling Monitor Mode

```
sudo airmon-ng start wlan0
```

#### Performing the Attack

To begin, we scan our target access point using `airodump-ng` and capture the communication into a file. We specify our interface in monitor mode with `wlan0mon`, the channel our access point is running on with `-c`, and the location to save the capture file with the `-w` argument.

```
airodump-ng wlan0mon -c 1 -w WEP
```


Next, we initiate the `KoreK chop chop` attack in a second terminal. The source MAC address used should be capable of associating with the network. If we need to conduct the attack without authentication and association, there are two options: either omit the `-h` flag (though this can result in dropped packets), or specify the MAC address of an already connected station, which tends to be more reliable. The `-4` option in `aireplay-ng` is used for the KoreK chop chop attack.

Similar to fragmentation attacks, we want to capture a packet originating from a connected station and destined for the AP. Once a valid packet is found, we approve the selection and start the attack, retrieving the PRGA keystream bit by bit.

```
aireplay-ng -4 -b C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C wlan0mon
```

Now, analyze the decrypted packet to identify the source and destination IP addresses.

```
tcpdump -s 0 -n -e -r replay_dec-0805-221220.cap
```

After identifying the required IP addresses, we can forge an ARP request using `packetforge-ng`. In this command, we specify the access point's MAC address with `-a`, the station’s MAC address with `-h`, the access point’s IP address with `-k`, the station’s IP address with `-l`, the location and name of our PRGA file with `-y`, and finally, the output name for the forged ARP request capture file with `-w`.

```
packetforge-ng -0 -a C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C -k 192.168.1.1 -l 192.168.1.75 -y replay_dec-0805-221220.xor -w forgedarp.cap
```

```
aireplay-ng -2 -r forgedarp.cap -h 7E:8D:FC:DD:D7:2C wlan0mon
```

As this process runs, back in the `airodump-ng` output we can notice that the **Frames** count for the connected station increases. This is a positive sign that many new IVs are being generated.

We can wait until enough packets have been generated before attempting to crack the WEP key. Additionally, to further accelerate the IV generation process, we can use an ARP request replay attack in a new terminal. This approach will expedite the overall process.

```
aireplay-ng -3 -b C8:D1:4D:EA:21:A6 -h 7E:8D:FC:DD:D7:2C wlan0mon
```


Once we have generated enough packets, we can use `aircrack-ng` to crack the WEP key using the captured Initialization Vectors (IVs) stored in the `WEP-01.cap` file.

```
aircrack-ng -b C8:D1:4D:EA:21:A6 WEP-01.cap 
```


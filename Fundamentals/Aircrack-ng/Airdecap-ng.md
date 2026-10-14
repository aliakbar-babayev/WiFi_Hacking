[Airdecap-ng](https://www.aircrack-ng.org/doku.php?id=airdecap-ng) is a valuable tool for decrypting wireless capture files once we have obtained the `key` to a network. It can decrypt `WEP`, `WPA PSK`, and `WPA2 PSK` captures. Additionally, it can remove wireless headers from an `unencrypted` capture file. This tool is particularly useful in analyzing the data within captured packets by making the content readable and removing unnecessary wireless protocol information.

`Airdecap-ng` generates a new file with the suffix `-dec.cap,` which contains the decrypted or stripped version of the original input file. For instance, an input file named `HTB-01.cap` will result in an unencrypted output file named `HTB-01-dec.cap`.

In the encrypted capture file created using `airodump-ng` and opened using Wireshark as shown below, the `Protocol` tab only displays `802.11` without specifying the actual protocol of the message. Similarly, the `Info` tab does not provide meaningful information. Additionally, the `source` and `destination` fields only contain MAC addresses instead of the corresponding IP addresses.

Conversely, in the decrypted capture file using `airdecap-ng`, observe how the `Protocol` tab displays the correct protocol, such as ARP, TCP, DHCP, HTTP, etc. Additionally, notice how the `Info` tab provides more detailed information, and it correctly displays the `source` and `destination` IP addresses.



### Removing Wireless Headers from Unencrypted Capture file

Capturing packets on an open network would result in an `unencrypted` capture file. Even if the capture file is already unencrypted, it may still contain numerous frames that are not relevant to our analysis. To streamline the data, we can utilize `airdecap-ng` to eliminate the wireless headers from an unencrypted capture file.

To remove the wireless headers from the capture file using Airdecap-ng, we can use the following command:

```
airdecap-ng -b <bssid> <capture-file>
```

### Decrypting WEP-encrypted captures

Airdecap-ng is a powerful tool for decrypting WEP-encrypted capture files. Once we have obtained the hexadecimal `WEP key`, we can use it to decrypt the captured packets. This process will remove the wireless encryption, allowing us to analyze the data.

```
airdecap-ng -w <WEP-key> <capture-file>
```

Open networks are vulnerable to eavesdropping because their traffic is not encrypted. To address this, Wired Equivalent Privacy (WEP) was introduced in 1997 as part of the [IEEE 802.11](https://www.ieee802.org/11/) standard. It aimed to provide a level of privacy for data transmitted over wireless networks.

WEP, being an older standard, offers valuable lessons for us when dealing with communication ciphers. It has since been replaced by Wi-Fi Protected Access, but can still be found in some business environments. WEP makes use of initialization vectors (IVs), a 40-bit or 104-bit shared key (also referred to as the WEP key), the Rivest Cipher 4 (RC4) algorithm, and cyclic redundancy checks (CRC32) to provide encryption for wireless communications. When WEP was developed, it originally incorporated a 24-bit initialization vector due to U.S. government export restrictions on cryptographic technologies, which limited key sizes. After these restrictions were lifted, WEP was updated to support a 128-bit encryption key, but incidentally it continued to use the same 24-bit initialization vector.

Although WEP held firm as a standard for a while, the discovery of different attacks led to multiple ways of compromising the shared key. This is due to the initialization vectors and cyclic redundancy checks used in the overall cipher. Regardless of whether WEP uses a 64-bit or 128-bit encryption key, the IV remains 24 bits. As a result, the algorithm is prone to repeated IVs during transmission. This has since enabled adversaries to construct decryption tables and retrieve the key with a high degree of statistical certainty, typically through packet building and replay attacks.


### Initialization Vector (IV)

#### The problem it solves

RC4 is a **stream cipher**. It takes a key and generates a pseudo-random stream of bytes (the _keystream_), which is XORed with your plaintext:

```
Ciphertext = Plaintext ⊕ Keystream
```

The critical rule of stream ciphers: **never reuse the same keystream.** If you do, an attacker can XOR two ciphertexts together and the keystream cancels out:

```
C1 = P1 ⊕ K
C2 = P2 ⊕ K
C1 ⊕ C2 = P1 ⊕ P2     ← keystream gone; attacker now has a relationship between two plaintexts
```

If the attacker knows or can guess one plaintext (and in Wi-Fi, lots of packet headers are predictable, like ARP or DHCP), they instantly recover the other.

#### The IV’s job

In WEP, every device on the network shares **one static key**. If RC4 were seeded with only that key, every packet would use the identical keystream, which is a disaster. The IV is a small value that gets **mixed with the key to make each packet’s keystream different**:

```
RC4 seed = IV (24 bits) || WEP key (40 or 104 bits)
```

The IV is sent **in plaintext** in the packet header, so the receiver can combine it with the shared key and generate the same keystream.

```
[ 802.11 header ][ IV (3 bytes, cleartext) ][ encrypted payload + ICV ]
```


## WEP Authentication

WEP supports two types of authentication systems: `Open` and `Shared`. In open authentication, a client does not provide any credentials when connecting to the access point (AP). However, to encrypt and decrypt data frames, the client must have the correct key.

In shared authentication, a challenge text is sent to the client during the authentication process. The client must encrypt this challenge text with the WEP key and send it back to the AP for verification. This process allows the client to prove that it knows the key. Upon receiving the encrypted challenge text, the AP attempts to decrypt it. If the decryption is successful and the decrypted text matches the original challenge text, the client is permitted to associate with the access point.

![Diagram showing a four-step authentication process between Client and AP: 1. Client sends Authentication Request to AP. 2. AP sends Challenge to Client. 3. Client sends Challenge Response to AP. 4. AP confirms Success or Failure to Client.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/Wep_process.png)

Below is a step-by-step description of the shared WEP authentication process, which can be visualized in the diagram above:

1. `Authentication Request`: The process begins with the client sending an authentication request to the access point.
2. `Challenge`: The access point responds with a custom authentication response that includes challenge text for the client.
3. `Challenge Response`: The client then replies with the encrypted challenge, which is encrypted using the WEP key.
4. `Verification`: The AP decrypts the challenge, and sends back an indication of success or failure.
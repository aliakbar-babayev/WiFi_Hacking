
Wired Equivalent Privacy utilizes a standard [CRC32 checksum](https://fuchsia.googlesource.com/third_party/wuffs/+/HEAD/std/crc32/README.md), which is computed over the packet plaintext and subsequently appended to it. The combined plaintext/checksum block is then XORed with the RC4 keystream to produce the final ciphertext. The `KoreK Chop Chop Attack` is notorious for abusing the CRC32 hashing function to decrypt a packet without knowing the key. Simply put, this is done by removing a byte of the final ciphertext, calculating the new ICV, then sending the modified packet back to the network. Based on the network's response (whether the packet is accepted or rejected), the attacker can infer the byte's true value. By repeating this process for each byte, the attacker can gradually decrypt the entire packet. We will explore this in further detail later.

Generally, the CRC32 hashing algorithm is the following:

`g(x) = x32 + x26 + x23 + x22 + x16 + x12 + x11 + x10 + x8 + x7 + x5 + x4 + x2 + x + 1`

![Diagram showing CRC32 process: Packet Plain Text and Checksum combine to form Packet Plain Text + Checksum, processed by CRC32.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/185/Diagrams/wep_2.png)



CRC32 is an **error-detection** algorithm. It treats the message as a giant binary polynomial, divides it by a fixed 32-bit polynomial, and the remainder is the checksum. It’s designed to catch **accidental** corruption like bit flips from noise.

In WEP, a CRC32 of the plaintext is computed and appended as the **Integrity Check Value (ICV)**, then encrypted along with the data:

```
Plaintext payload → compute CRC32 → append ICV → XOR with RC4 keystream → send
```


#### Why it fails as a security measure

CRC32 is **not a cryptographic hash or MAC.** It has no secret key. It provides integrity against random noise but nothing against a deliberate attacker. Two properties break it:

**a) CRC is linear**

For CRC: `CRC(A ⊕ B) = CRC(A) ⊕ CRC(B)` (with some constant adjustments for equal-length messages).

Combine this with the stream cipher’s malleability, where flipping a ciphertext bit flips the same plaintext bit, and you get a **bit-flipping attack**:

1. Attacker intercepts an encrypted packet.
2. They choose a change they want, Δ (e.g., flip certain bits in the payload).
3. They compute `CRC(Δ)`, which is easy since CRC is public and keyless.
4. They XOR Δ into the encrypted payload and `CRC(Δ)` into the encrypted ICV.
5. The ICV still validates, because of linearity.

The attacker modified the message **without knowing the key** and the receiver accepts it as authentic.

**b) No key involved in the integrity check**

Because CRC32 uses a public polynomial and no secret, anyone can recompute it for any message. This also allows **packet injection** once the attacker has recovered even a single keystream for a given IV: they can craft a valid packet with a correct ICV and encrypt it.

**c) It enables chopchop-style attacks**

The Korek “chopchop” attack exploits the CRC structure: the attacker truncates an encrypted packet by one byte, guesses the missing byte, and uses the receiver’s accept/reject response (via the ICV check) as an oracle to decrypt the packet one byte at a time, again without the key.
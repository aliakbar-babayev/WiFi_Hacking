#### Why WEP’s IV design was broken

**a) Too small: 24 bits = 16,777,216 possible values**

That sounds large, but consider the birthday paradox. On a busy network sending thousands of packets per second, IVs start repeating in a matter of **hours**, sometimes minutes. With a 50% collision chance after only about 5,000 packets, an attacker can collect repeated-IV packets (same keystream) and apply the XOR trick above.

**b) No rule for how IVs are chosen**

Many implementations used a simple counter starting from 0, or reset the IV to 0 every time the card was initialized. That means keystream reuse was practically guaranteed.

**c) The IV is part of the RC4 key, which exposes weaknesses in RC4 itself**

This is the most damaging flaw. In 2001, Fluhrer, Mantin, and Shamir (the **FMS attack**) showed that RC4’s key scheduling algorithm leaks information about the key when certain “weak IVs” are used. Because the IV is **prepended to the key and sent in the clear**, the attacker sees the first part of the RC4 key for every packet. By collecting enough packets with weak IVs, they statistically recover the secret key byte by byte. Later improvements (KoreK, PTW attack) reduced the packets needed from millions to **tens of thousands**, which means cracking WEP in under a minute with modern tools.

**d) Key size doesn’t help**

The “128-bit WEP” is really 104-bit key + 24-bit IV. Since the IV size didn’t change, the keystream-reuse problem is identical. A longer key doesn’t fix a short IV.
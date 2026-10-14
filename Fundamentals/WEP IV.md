
## WEP IV (Initialization Vector) — Explained

### The Basic Problem It’s Trying to Solve

WEP encrypts data using a stream cipher called **RC4**. Here’s the core issue with any stream cipher: if you encrypt two different pieces of data with the _exact same key_, you create a serious vulnerability — an attacker who gets both encrypted outputs can XOR them together and start recovering information about the original data (and potentially the key itself), because the “keystream” repeats.

Since a WiFi network’s actual password-derived key stays the same for a long time (you don’t change your WiFi password every packet), encrypting thousands of packets with that _exact same static key_ would be catastrophically weak — every single packet would reuse the identical keystream.

### The IV’s Job

The **IV (Initialization Vector)** is a value that gets mixed in with the static key to produce a _different_ effective encryption key for every single packet, even though the underlying password never changes.

Per-packet encryption key = IV + Static WEP Key


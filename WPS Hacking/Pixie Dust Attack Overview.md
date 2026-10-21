
Some vendors such as Ralink, Realtek, MediaTek, and Broadcom are susceptible to offline bruteforcing techniques through the `Pixie Dust Attack`. This is due to bad randomization during nonce generation. The E-S1 and E-S2 nonce values are 128-bits. As such, if we were to try to blindly bruteforce the hash values through variable brute force, this would take a very long time. Due to certain vendors having bad/predictable nonce value generation, we can retrieve these values, which makes bruteforcing on the E-Hash1 and E-Hash2 values much quicker. This helps eliminate the need to conduct online bruteforcing through every iteration of a possible PIN.

If we recall, during the M1 and M2 messages, the PKe and PKr values are shared between the enrollee (client) and registrar (AP), respectively. Additionally, during the M3 message, we receive the E-Hash1 and E-Hash2 values. Simply put, the E-Hash1 and E-Hash2 values are structured as shown below.

- `E-Hash1 = (E-S1 nonce value | PSK1 | PKe | PKr)`
- `E-Hash2 = (E-S2 nonce value | PSK2 | PKe | PKr)`

During the initial message exchange with the access point, we already know the PKe and PKr values. To crack these HMAC-SHA-256 hashes, we need to guess the E-S1 and E-S2 nonce values, as the resulting values will form both portions of our PIN (the PSK1 and PSK2 values).

In order to elaborate on Pixie Dust attacks and bad random nonce generation, these next few examples will help, but are not exhaustive.

1. Certain Ralink and Mediatek chipsets contain the same zero nonce generation issue for WPS. This means that the nonce values are never generated, and instead are always set to zero. As such, we know all values except the PSK1 and PSK2 values respectively.

- `E-Hash1 = (E-S1 (0) | PSK1 | PKe (known) | PKr (known) )`
- `E-Hash2 = (E-S2 (0) | PSK2 | PKe (known) | PKr (known) )`

2. Certain Broadcom chipsets use the same random number generation algorithm to generate the nonce values, as well as other values such as the N1 enrollee nonce or PKe. Since these values are generated using the same algorithm, bruteforcing looks like the following.

- `We guess all seed values until we find the correct ones that generated the N1 enrollee nonce or PKe value, then generate the respective E-S1 and E-S2 nonce values.`
- `We are then able to retrieve the PSK1 and PSK2 values.`

3. Similarly, certain Realtek chipsets have issues with how they generate seeds for random values. These vulnerable chipsets utilize Unix timestamps from the WPS EAP message exchange as seed values for generating the E-S1, E-S2, and PKe enrollee values. With most timing-based attacks, depending on the delay and speed of message delivery, these values are often identical or differ by only a small increment. Overall, the process looks like the following:

- `E-S1 = E-S2 = PKe or E-S1 = E-S2 = PKe + N`
- `Due to the weak random (Unix timestamp) seed, the E-S1, E-S2, and PKe values are often identical, or incrementally different by a small value, N.`
- `We increment through guesses of the seed values that were used to generate the PKe. This then allows us to guess the E-S1 and E-S2 values, respectively.`
- `We are then able to retrieve the PSK1 and PSK2 values respectively.`

Not all Pixie Dust attacks are equal, but generally they are much quicker to conduct than traditional online brute-forcing techniques. This is due to us guessing the nonce values, rather than guessing one of the possible 11,000 PIN combinations. By doing so, we can retrieve the correct PIN within a few seconds to a couple hours, as opposed to waiting several hours for an online attempt to potentially succeed. Another advantage of Pixie Dust attacks is the low number of PIN guesses required. For access points with locking mechanisms, this can be tremendously beneficial when attempting to avoid being locked out.
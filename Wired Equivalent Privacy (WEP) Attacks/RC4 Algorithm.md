
In cryptography, `RC4 (Rivest Cipher 4)`, also known as `ARC4` or `ARCFOUR (Alleged RC4)`, is a stream cipher. It was designed by Ron Rivest of [RSA Security](https://en.wikipedia.org/wiki/RSA_Security) in 1987 and became part of several commonly used encryption protocols and standards (including WEP) due to its simplicity and high speed.

RC4 is a symmetric cipher, which means the same key is used for both encryption and decryption. It generates a stream of bits that are XORed with the plaintext to produce the ciphertext. To decrypt the data, the ciphertext is XORed with the same key stream to recover the plaintext.

RC4 consists of two key components:

1. Key Scheduling Algorithm (KSA)
2. Pseudo Random Generation Algorithm (PRGA)

The `Key Scheduling Algorithm` initializes the state table using the WEP key and the initialization vector (IV). The `Pseudo Random Generation Algorithm` produces the keystream used for the encryption and decryption process. In the upcoming section, we will delve deeper into the RC4 algorithm, exploring its mechanisms and functionality in greater detail.


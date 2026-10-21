WPS works by establishing authentication through a series of [Extensible Authentication Protocol (EAP)](https://en.wikipedia.org/wiki/Extensible_Authentication_Protocol) messages. Some of the information communicated includes Public Keys, PINs, and nonce values. Essentially, after some checks and balances between the access point and the connected client, the access point (registrar) shares the WPA pre-shared key, which allows the connected client (enrollee) to ensure communications as normal with WPA. It should also be noted that when WPS (Wi-Fi Protected Setup) is used to configure an access point, the roles of the access point (AP) and the client device can switch. In this case, the AP may act as the Enrollee, while the client device assumes the role of the Registrar, which is responsible for [configuring the AP](https://android.googlesource.com/platform/external/wpa_supplicant_8/+/master/wpa_supplicant/README-WPS#36).


### WPS PIN Anatomy

The WPS PIN is eight digits in length and consists of two primary portions. The first portion is used in the M4 and M5 EAP messages, and the second portion is used in the M6 and M7 EAP messages. Each of these portions is four digits in length. Most would assume that there would be 100,000,000 (108) possible digit combinations, but in the case of WPS, this is not true. There are only 11,000 possible combinations.

![Table with two sections: First Half showing 1023, Second Half showing 987 and 5.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/186/WPSAlgorithm/PIN/WPS_PIN.png)

This is due to how the PIN functions. The first half only has 104 possible combinations and the second half has only 103 possible combinations. The last digit of the second half is used as a checksum and can be easily calculated. Therefore, there are only 10,000 (104) + 1,000(103) possible digit combinations, which is 11,000 total combinations.


### WPS EAP Messages

Before describing the series of EAP messages, the following definitions will come in handy.

|Name|Definition|
|---|---|
|`PKe`|This is the Enrollee's (Access Point's) Diffie-Hellman public key.|
|`PKr`|This is the Registrar's (Station's/Client's) Diffie-Hellman public key.|
|`PSK1`|First four-digit portion of the PIN (10,000 possible combinations).|
|`PSK2`|Second four-digit portion of the PIN (1,000 possible combinations). The last digit is used as the checksum.|
|`KDK (Key Derivation Key)`|This is a key used in derivation for the auth key.|
|`KWK (Key Wrap Key)`|Used in the process of encrypting messages with AES.|
|`E-S1`|This is a secret 128-bit enrollee (AP) nonce value used in derivation for E-Hash1.|
|`E-S2`|This is a secret 128-bit enrollee (AP) nonce value used in derivation for E-Hash2.|
|`R-S1`|This is a secret 128-bit registrar (client/station) nonce value used in derivation for R-Hash1.|
|`R-S2`|This is a secret 128-bit registrar (client/station) nonce value used in derivation for R-Hash2.|
|`E-Hash1 (Enrollee Hash1)`|Comprised of the E-S1 nonce value, PSK1, PKe, and PKr values. Created through the HMAC-SHA-256 hashing function using the Auth Key.|
|`E-Hash2 (Enrollee Hash2)`|Comprised of the E-S2 nonce value, PSK2, PKe, and PKr values. Created through the HMAC-SHA-256 hashing function using the Auth Key.|
|`R-Hash1 (Registrar Hash1)`|Comprised of the R-S1 nonce value, PSK1, PKe, and PKr values. Created through the HMAC-SHA-256 hashing function using the Auth Key.|
|`R-Hash2 (Registrar Hash2)`|Comprised of the R-S2 nonce value, PSK2, PKe, and PKr values. Created through the HMAC-SHA-256 hashing function using the Auth Key.|
|`Auth Key`|Derived from the KDK, PSK1, and PSK2 values.|
|`WPA-PSK`|This is the final disclosed pre-shared key (aka password) used to authenticate the client.|

The series of EAP messages from a high level looks like the following:

![Diagram of EAPOL communication between Access Point (Enrollee) and Station (Registrar) showing steps: EAPOL-Start, EAP Request Identify, EAP Response Identity, EAP Requests and Responses M1 to M8 with credentials, EAP NACK, and EAP Acknowledgement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/186/WPSAlgorithm/EAPSeries/WPS_EAP.png)


Each of these messages is responsible for disclosing different information, and they conduct the following.

|Message|Description|
|---|---|
|`EAPOL-Start`|The connected client initiates the series of EAP messages.|
|`EAP Request Identity`|The access point requests the connected client's identity.|
|`EAP Response Identity`|The client sends the access point its identity as requested.|
|`EAP M1 Message`|The access point sends the client their Diffie-Hellman public key (PKe).|
|`EAP M2 Message`|The client then sends the Access point the their Diffie-Hellman public key (PKr).|
|`EAP M3 Message`|The access point sends the client the E-Hash1 and E-Hash2 values.|
|`EAP M4 Message`|The client then sends the access point the R-Hash1, R-Hash2, and R-S1 nonce value encrypted with AES.|
|`EAP M5 Message`|The access point sends the client the E-S1 nonce value encrypted with AES.|
|`EAP M6 Message`|The client sends the access point the R-S2 nonce value encrypted with AES.|
|`EAP M7 Message`|If the PIN is correct, the access point sends the client the E-S2 value and the WPA-PSK encrypted with AES.|
|`EAP M8 Message`|The client then sends the WPA-PSK back to the access point to begin the WPA handshake process.|

These EAP messages are simple yet somewhat complex. Fortunately for us, two different cracking methods can be employed to guess the correct PIN (through all 11,000 possible combinations) and retrieve the final WPA-PSK. These methods are online brute-forcing and offline brute-forcing, also known as the Pixie Dust Attack
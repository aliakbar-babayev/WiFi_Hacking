

There are two primary authentication systems commonly used in WiFi networks: `Open System Authentication` and `Shared Key Authentication`.

![Flowchart of Authentication Methods: Open Key and Shared Key. Open Key includes WEP, which is obsolete and uses RC4 and CRC-32. Shared Key includes WPA, using TKIP and MIC, and 802.11i/WPA2, using AES and CCM.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/auth_methods_.png)



### Open System Authentication

As the name implies, open system authentication does not require any shared secret or credentials right away. This authentication type is commonly found for open networks that do not require a password. For Open System Authentication, it tends to follow this order:

1. The client (station) sends an authentication request to the access point to begin the authentication process.
2. The access point then sends the client back an authentication response, which indicates whether the authentication was accepted.
3. The client then sends the access point an association request.
4. The access point then responds with an association response to indicate whether the client can stay connected.

![Diagram showing communication between Client and AP: Authentication Request, Authentication Response, Association Request, and Association Response.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/Open_system.png)



### Shared Key Authentication

On the other hand shared key authentication does involve a shared key, as the name implies. In this authentication system, the client and access point prove their identities through the computation of a challenge. This method is often associated with Wired Equivalent Privacy (`WEP`) and Wi-Fi Protected Access (`WPA`). It provides a basic level of security through the use of a pre-shared key.

![Table of Shared Key Authentication Methods: WEP uses pre-shared key, RC4, CRC-32, and is weak. WPA uses PSK or 802.1x, TKIP, MIC, and is strong. 802.11i/WPA2 uses PSK or 802.1x, AES, CCMP, and is stronger.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/Shared_auth.png)



#### Authentication with WEP

1. `Authentication request:` Initially, as it goes, the client sends the access point an authentication request.
2. `Challenge:` The access point then responds with a custom authentication response which includes challenge text for the client.
3. `Challenge Response:` The client then responds with the encrypted challenge, which is encrypted with the WEP key.
4. `Verification:` The AP then decrypts this challenge and sends back either an indication of success or failure.

![Diagram showing communication between Client and AP: Authentication Request, Challenge, Challenge Response, and Confirm Success/Failure.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/Wep_process.png)

---

#### Authentication with WPA

On the flip side, WPA utilizes a form of authentication that includes a four-way handshake. Commonly, this replaces the association process with more verbose verification, and in the case of WPA3, the authentication portion is even crazier for the pairwise key generation. From a high level, this is performed like the following.

1. `Authentication Request:` The client sends an authentication request to the AP to initiate the authentication process.
2. `Authentication Response:` The AP responds with an authentication response, which indicates that it is ready to proceed with authentication.
3. `Pairwise Key Generation:` The client and the AP then calculate the PMK from the PSK (password).
4. `Four-Way Handshake:` The client and access point then undergo each step of the four way handshake, which involves nonce exchange, derivation, among other actions to verify that the client and AP truly know the PSK.

![Diagram showing communication between Client and AP: Authentication Request, Authentication Response, Pairwise Key Generation, and 4-Way Handshake.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/222/Auth_Methods/Wpa_process.png)

Shared key authentication type also involves [WPA3](https://documentation.meraki.com/MR/Wi-Fi_Basics_and_Best_Practices/WPA3_Encryption_and_Configuration_Guide), the latest and most secure WiFi security standard. WPA3 introduces significant improvements over its predecessors, including more robust encryption and enhanced protection against brute force attacks. One of its key features is `Simultaneous Authentication of Equals (SAE)`, which replaces the `Pre-Shared Key (PSK)` method used in WPA2, providing better protection for passwords and individual data sessions.

Despite its advantages, WPA3 adoption has been slower due to hardware restrictions. Many existing devices do not support WPA3 and require firmware updates or replacements to be compatible. This creates a barrier to widespread implementation, particularly in environments with a large number of legacy devices. Consequently, while WPA3 offers superior security, its use is not yet widespread, and many networks continue to rely on older standards like WPA2 until the necessary hardware upgrades become more accessible and affordable.
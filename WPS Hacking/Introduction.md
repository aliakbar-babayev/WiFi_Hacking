# Wi-Fi Protected Setup Overview

---

WPS was originally developed by Cisco in 2006 as a method to enable convenience and ease of use for users with little knowledge. Either through the push of a button or entering of a PIN users are able to easily connect their devices to their wireless network. Since then, multiple different exploitation tools have been developed with the intent to abuse the PIN. WPS PINs are eight digits in length, making them significantly easier to crack compared to traditional WPA methods.

Although convenient, WPS is susceptible to online PIN cracking and offline PIN cracking methods. WPS utilizes a series of EAP messages exchanged between a station (enrollee) and an access point (registrar). During this process, valuable information is disclosed; information that can be exploited for these attack methods. While traditional online PIN cracking takes hours to complete, offline PIN cracking can be as quick as a few minutes when the access point is vulnerable.

WPS utilizes HMAC-SHA-256, which is considered a fairly secure hashing function. However, due to the lack of possible PIN combinations, randomness in nonce values, and information disclosed in the communications between the access point and the client, we are able to crack these PINs relatively quickly and retrieve the PSK for normal WPA communications.

When assessing wireless access points, it is always important to check for WPS vulnerabilities. As such, possessing the skills to test for WPS-related vectors is crucial for all wireless penetration testers.

---

### WPS Connection Methods

There are four methods to connect to a WPS-enabled access point. Each of them is detailed below:

|Method|Description|
|---|---|
|`Push Button Configuration (PBC)`|This is the most common method and involves pressing a physical or virtual button on the router and the client device. Once the button is pressed on both devices, they automatically exchange the necessary information to establish a secure connection.|
|`PIN Entry`|Each WPS-enabled device has an 8-digit PIN code, either provided by the manufacturer or displayed on the device. Users enter this PIN on their router or access point’s configuration page to connect the device to the network.|
|`Near-field communication method`|Some devices support NFC, allowing users to tap the device on the router to establish a connection. This method is less common but offers an additional level of convenience.|
|`USB Flash Drive`|Involves transferring configuration settings via a USB drive from the router to the client device. This method is rarely used due to the inconvenience compared to other methods.|

---

### Benefits of WPS

- `Ease of Use`: Simplifies the process of adding new devices to a wireless network, making it accessible even for non-technical users.
- `Convenience`: Eliminates the need to remember or enter long and complex passwords.

---

### Security Concerns

While WPS was designed to make network connections simpler, it has notable security vulnerabilities:

- `PIN Method Vulnerability`: The 8-digit PIN can be cracked relatively easily through brute-force attacks due to the way the protocol verifies the PIN in two halves.
- `Physical Security Risks`: The PBC method relies on physical security, meaning an unauthorized person within range could potentially push the button and connect to the network.



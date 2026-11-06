#!/usr/bin/env python3
"""WiFi Hacking Quiz 1: Fundamentals & Aircrack-ng Suite"""

import random

QUESTIONS = [
    {
        "q": "What are the three main 802.11 frame types and their binary identifiers?",
        "options": [
            "Management (00), Control (01), Data (10)",
            "Beacon (00), Probe (01), Auth (10)",
            "Management (01), Control (10), Data (11)",
            "Data (00), Control (01), Management (10)"
        ],
        "answer": 0,
        "explain": "Management frames (00) handle association/auth, Control frames (01) manage access, Data frames (10) carry payloads."
    },
    {
        "q": "Why can deauthentication frames be forged in WPA2 but NOT in WPA3?",
        "options": [
            "WPA3 encrypts all frames including deauth",
            "WPA3 uses Protected Management Frames (PMF/802.11w) which signs management frames",
            "WPA3 doesn't use deauthentication frames at all",
            "WPA2 sends deauth in plaintext while WPA3 uses TLS"
        ],
        "answer": 1,
        "explain": "WPA2 deauth frames are unsigned and unverified — anyone can forge them. WPA3 mandates 802.11w (PMF), which cryptographically protects management frames."
    },
    {
        "q": "What is the subtype binary code for Beacon frames?",
        "options": [
            "0100",
            "1100",
            "1000",
            "0001"
        ],
        "answer": 2,
        "explain": "Beacon frames are subtype 1000. APs broadcast beacons ~10 times/sec advertising SSID, ciphers, auth types, and data rates."
    },
    {
        "q": "What interface mode captures ALL wireless traffic regardless of intended recipient?",
        "options": [
            "Managed Mode",
            "Master Mode",
            "Ad-hoc Mode",
            "Monitor Mode"
        ],
        "answer": 3,
        "explain": "Monitor mode is promiscuous — it captures every frame on the channel. Essential for WiFi pentesting."
    },
    {
        "q": "Which command enables monitor mode using the aircrack-ng suite?",
        "options": [
            "airmon-ng enable wlan0",
            "sudo airmon-ng start wlan0",
            "aireplay-ng --monitor wlan0",
            "airodump-ng -m wlan0"
        ],
        "answer": 1,
        "explain": "airmon-ng is the monitor mode manager. 'start' creates wlan0mon. You can also specify a channel: 'sudo airmon-ng start wlan0 11'."
    },
    {
        "q": "What encryption does WPA2 use versus WPA?",
        "options": [
            "WPA2: TKIP + MIC, WPA: AES + CCMP",
            "WPA2: AES + CCMP, WPA: TKIP + MIC",
            "Both use AES but WPA2 has longer keys",
            "WPA2: SAE, WPA: AES + CCMP"
        ],
        "answer": 1,
        "explain": "WPA uses TKIP + MIC (weaker). WPA2 upgraded to AES + CCMP. WPA3 uses SAE (Simultaneous Authentication of Equals)."
    },
    {
        "q": "In airodump-ng output, what does a hidden SSID look like?",
        "options": [
            "[HIDDEN]",
            "***",
            "<length: x> where x is the SSID length",
            "(empty string)"
        ],
        "answer": 2,
        "explain": "Hidden SSIDs appear as '<length: x>' notation. The AP still broadcasts beacons but with the SSID field zeroed out."
    },
    {
        "q": "What aireplay-ng attack mode number is deauthentication?",
        "options": [
            "1",
            "3",
            "0",
            "5"
        ],
        "answer": 2,
        "explain": "Mode 0 = deauth, 1 = fake auth, 2 = interactive replay, 3 = ARP replay, 4 = chopchop, 5 = fragmentation, 6 = cafe latte."
    },
    {
        "q": "What does the airgraph-ng CAPR graph show, and what does the color GREEN represent?",
        "options": [
            "Client probe requests; GREEN = strong signal",
            "Client-to-AP relationships; GREEN = WPA encryption",
            "Channel allocation; GREEN = available channels",
            "Client-to-AP relationships; GREEN = Open network"
        ],
        "answer": 1,
        "explain": "CAPR = Clients to AP Relationship. Colors: Green=WPA, Yellow=WEP, Red=Open, Black=Unknown."
    },
    {
        "q": "What is the minimum EAPOL handshake data needed by aircrack-ng to crack a WPA key?",
        "options": [
            "All 4 messages of the handshake",
            "Messages 1 and 2 only",
            "Messages 2+3, or 3+4",
            "Only message 2 (contains the MIC)"
        ],
        "answer": 2,
        "explain": "Aircrack-ng needs EAPOL packets 2+3 or 3+4. Not all 4 messages are required."
    },
    {
        "q": "What does airdecap-ng do?",
        "options": [
            "Captures encrypted packets from the air",
            "Decrypts WEP/WPA/WPA2 capture files offline",
            "Removes encryption from live traffic",
            "Cracks WEP keys from IV files"
        ],
        "answer": 1,
        "explain": "airdecap-ng decrypts captured .cap files after you already know the key. Output has '-dec.cap' suffix."
    },
    {
        "q": "What four file formats does airodump-ng create when saving with the -w flag?",
        "options": [
            ".cap, .csv, .xml, .json",
            ".pcap, .txt, .log, .html",
            ".cap, .csv, .kismet.csv, .kismet.netxml (+ .log.csv)",
            ".cap, .ivs, .csv, .pcap"
        ],
        "answer": 2,
        "explain": "airodump-ng creates .cap, .csv, .kismet.csv, .kismet.netxml, and .log.csv files."
    },
    {
        "q": "You need to scan 5GHz WiFi networks. What airodump-ng flag do you use?",
        "options": [
            "--freq 5",
            "-c 36-165",
            "--band a",
            "--5ghz"
        ],
        "answer": 2,
        "explain": "'--band a' scans the 5GHz band. By default airodump-ng only scans 2.4GHz."
    },
    {
        "q": "What is the correct order of the WPA 4-way handshake?",
        "options": [
            "Client sends Snonce → AP sends Anonce → AP sends GTK → Client ACK",
            "AP sends Anonce → Client sends Snonce+MIC → AP sends GTK+MIC → Client ACK",
            "AP sends GTK → Client sends MIC → AP verifies → Key installed",
            "Client requests key → AP sends PMK → Client derives PTK → AP confirms"
        ],
        "answer": 1,
        "explain": "Msg1: AP→Anonce, Msg2: Client→Snonce+MIC, Msg3: AP→GTK+MIC, Msg4: Client→ACK (key installation)."
    },
    {
        "q": "What daemon is required to run a wireless interface in Master (AP) mode?",
        "options": [
            "wpa_supplicant",
            "NetworkManager",
            "hostapd",
            "dnsmasq"
        ],
        "answer": 2,
        "explain": "hostapd is the AP management daemon. It handles authentication and manages the BSS in Master mode."
    },
    {
        "q": "What aireplay-ng flag runs an injection test to verify your card can inject packets?",
        "options": [
            "-0",
            "--test",
            "-9",
            "Both --test and -9"
        ],
        "answer": 3,
        "explain": "aireplay-ng attack mode 9 is the injection test. Both '--test' and '-9' work."
    },
    {
        "q": "In Open System Authentication, how many steps are involved before a client is associated?",
        "options": [
            "2 (auth request, auth response)",
            "3 (auth request, auth response, association)",
            "4 (auth request, auth response, association request, association response)",
            "6 (including the 4-way handshake)"
        ],
        "answer": 2,
        "explain": "Open System Auth: auth request → auth response → association request → association response. No credentials needed."
    },
    {
        "q": "What tool and command do you use to connect to a WPA2 network from the command line?",
        "options": [
            "iwconfig wlan0 key <password> && dhclient wlan0",
            "wpa_passphrase \"ssid\" \"pass\" > file.conf && wpa_supplicant -B -i wlan0 -c file.conf && dhclient wlan0",
            "nmcli dev wifi connect ssid password pass",
            "iwconfig wlan0 essid ssid key s:password"
        ],
        "answer": 1,
        "explain": "wpa_passphrase generates a config, wpa_supplicant connects in background (-B), dhclient gets an IP."
    },
    {
        "q": "How often does an AP broadcast beacon frames?",
        "options": [
            "Once per second",
            "~10 times per second",
            "~100 times per second",
            "Only when clients probe"
        ],
        "answer": 1,
        "explain": "APs broadcast beacon frames approximately 10 times per second, advertising presence, SSID, and capabilities."
    },
    {
        "q": "What does the 'mesh' interface mode do, and how do you set it?",
        "options": [
            "Creates a repeater; 'iw dev wlan0 set type repeater'",
            "Self-configuring routing network; 'iw dev wlan0 set type mesh'",
            "Bridges two networks; 'brctl addif wlan0 mesh0'",
            "Enables multi-AP roaming; 'hostapd mesh.conf'"
        ],
        "answer": 1,
        "explain": "Mesh mode creates a self-configuring, decentralized routing network. Set with 'iw dev wlan0 set type mesh'."
    },
]


def run_quiz():
    print("=" * 65)
    print("  WiFi HACKING QUIZ 1: Fundamentals & Aircrack-ng Suite")
    print("=" * 65)
    print(f"\n  {len(QUESTIONS)} questions. Let's see what you know.\n")

    questions = QUESTIONS[:]
    random.shuffle(questions)
    score = 0
    wrong = []

    for i, q in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        print(f"  [{i}/{len(questions)}] {q['q']}\n")

        indices = list(range(len(q["options"])))
        random.shuffle(indices)
        correct_letter = None
        for j, idx in enumerate(indices):
            letter = chr(65 + j)
            if idx == q["answer"]:
                correct_letter = letter
            print(f"    {letter}) {q['options'][idx]}")

        while True:
            ans = input(f"\n  Your answer (A-{chr(64 + len(q['options']))}): ").strip().upper()
            if ans in [chr(65 + j) for j in range(len(q["options"]))]:
                break
            print("  Invalid input. Try again.")

        if ans == correct_letter:
            score += 1
            print(f"\n  ✓ Correct!")
        else:
            print(f"\n  ✗ Wrong. Correct answer: {correct_letter}")
            wrong.append(q)

        print(f"  → {q['explain']}")

    print(f"\n{'=' * 65}")
    print(f"  FINAL SCORE: {score}/{len(questions)} ({score * 100 // len(questions)}%)")
    print(f"{'=' * 65}")

    if wrong:
        print(f"\n  Review these {len(wrong)} topics:")
        for q in wrong:
            print(f"    • {q['q'][:80]}")
    elif score == len(questions):
        print("\n  Perfect score! You've nailed the fundamentals.")
    print()


if __name__ == "__main__":
    run_quiz()

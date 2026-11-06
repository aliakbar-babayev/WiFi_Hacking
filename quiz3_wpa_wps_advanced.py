#!/usr/bin/env python3
"""WiFi Hacking Quiz 3: WPA Cracking, WPS Hacking & Advanced Techniques"""

import random

QUESTIONS = [
    {
        "q": "The WPS PIN is 8 digits, but the effective keyspace is only 11,000. Why?",
        "options": [
            "Most vendors use the same first 5 digits",
            "The PIN is split into two halves (10,000 + 1,000) verified separately, and the 8th digit is a checksum",
            "The protocol only allows 11,000 attempts before lockout",
            "Digits 0-5 are never used in WPS PINs"
        ],
        "answer": 1,
        "explain": "PSK1 = first 4 digits (10,000 combos), PSK2 = next 3 digits (1,000 combos), 8th digit = checksum. Total: 11,000 instead of 100,000,000."
    },
    {
        "q": "What is the Pixie Dust attack and why does it work?",
        "options": [
            "It floods the AP with deauth packets until WPS resets",
            "It exploits weak/predictable nonce generation (E-S1, E-S2) in certain chipsets to derive the PIN offline",
            "It brute-forces the WPS PIN faster by using GPU acceleration",
            "It intercepts the WPS push-button signal wirelessly"
        ],
        "answer": 1,
        "explain": "Ralink/MediaTek set E-S1 and E-S2 to zero. Broadcom reuses the same RNG. Realtek uses Unix timestamps. All allow offline PIN computation."
    },
    {
        "q": "Which chipset vendors are vulnerable to Pixie Dust?",
        "options": [
            "Intel, Qualcomm, Atheros, Marvell",
            "Ralink, Realtek, MediaTek, Broadcom",
            "Cisco, Netgear, TP-Link, Asus",
            "All chipsets are equally vulnerable"
        ],
        "answer": 1,
        "explain": "Ralink/MediaTek (nonces = 0), Broadcom (same RNG for nonces and keys), Realtek (timestamps as seeds)."
    },
    {
        "q": "What WPS EAP message confirms the first half of the PIN is correct?",
        "options": [
            "M3 (AP sends E-Hash1, E-Hash2)",
            "M4 (Client sends R-Hash1, R-Hash2)",
            "M5 (AP sends E-S1 encrypted — first half verified)",
            "M7 (AP sends WPA-PSK)"
        ],
        "answer": 2,
        "explain": "M5 confirms PSK1 (first half). If wrong, AP sends NACK at M5. M7 delivers the WPA-PSK if the full PIN is correct."
    },
    {
        "q": "What tool do you use for WPS reconnaissance, and what does 'wps_locked = 2' mean?",
        "options": [
            "wash; locked=2 means AP is locked after too many attempts",
            "wash; locked=2 means AP is NOT locked",
            "reaver --scan; locked=2 means partially locked",
            "airodump-ng --wps; locked=2 means WPS version 2"
        ],
        "answer": 1,
        "explain": "'wash -i wlan0mon' does WPS recon. Counter-intuitively, wps_locked=2 means the AP is NOT locked."
    },
    {
        "q": "What is the Reaver command for a Pixie Dust attack?",
        "options": [
            "reaver -i mon0 -b <BSSID> -c <channel> --pixie",
            "reaver -K 1 -vvv -b <BSSID> -c 1 -i mon0",
            "reaver -i mon0 -b <BSSID> --offline-crack",
            "reaver -Z -b <BSSID> -i mon0 --dust"
        ],
        "answer": 1,
        "explain": "-K (or -Z) enables Pixie Dust mode. -vvv for verbose output. Much faster than online brute force."
    },
    {
        "q": "Important Reaver gotcha: why should you use 'iw' instead of 'airmon-ng' for monitor mode with Reaver?",
        "options": [
            "iw is faster at enabling monitor mode",
            "airmon-ng renames the interface which causes bugs in Reaver",
            "Reaver requires a specific monitor mode flag that only iw provides",
            "airmon-ng locks the channel and Reaver needs channel hopping"
        ],
        "answer": 1,
        "explain": "airmon-ng creates 'wlan0mon' which causes bugs. Using 'iw' keeps the original interface name."
    },
    {
        "q": "After getting a WPS PIN via Pixie Dust, how do you retrieve the WPA-PSK?",
        "options": [
            "The PIN IS the WPA password",
            "Run reaver again with the PIN: 'reaver -b <BSSID> -c 1 -p <PIN> -i mon0'",
            "Use aircrack-ng with the PIN as the key",
            "Connect to the AP with the PIN and run 'iwconfig' to see the PSK"
        ],
        "answer": 1,
        "explain": "Supply the discovered PIN with -p. Reaver completes the WPS exchange and the AP delivers the WPA-PSK in M7."
    },
    {
        "q": "What is hostapd-mana's 'karma attack'?",
        "options": [
            "It floods all nearby APs with deauth frames",
            "It answers 'yes' to any SSID probe request, so clients auto-connect to the rogue AP",
            "It poisons the ARP cache of connected clients",
            "It injects malicious beacon frames with fake SSIDs"
        ],
        "answer": 1,
        "explain": "Karma mode responds to ALL probe requests with 'yes, I am that network'. Clients with saved networks auto-connect."
    },
    {
        "q": "When using hostapd-mana for rogue AP WPA cracking, what format does mana_wpaout produce?",
        "options": [
            "Standard .cap file readable by aircrack-ng",
            "Binary .hccapx for hashcat",
            "Hashcat 22000 text format — aircrack-ng CANNOT read it directly",
            "John the Ripper format"
        ],
        "answer": 2,
        "explain": "mana_wpaout writes hashcat 22000 text format, NOT binary. You must strip the prefix: \"grep -oP 'WPA\\*02\\*.*' file > clean.hc22000\" then use hashcat -m 22000."
    },
    {
        "q": "For the rogue AP, should the interface be in monitor mode or managed mode?",
        "options": [
            "Monitor mode — it needs to capture all traffic",
            "Managed mode — hostapd needs a managed-mode interface to act as an AP",
            "Either works",
            "Master mode specifically"
        ],
        "answer": 1,
        "explain": "Common mistake: the interface must be in managed mode, NOT monitor mode. Check AP support with 'iw list | grep -A 10 \"Supported interface modes\"'."
    },
    {
        "q": "Two methods to find a hidden ESSID. One is deauth. What's the other, and when is deauth useless?",
        "options": [
            "Brute force with mdk3; deauth is useless against WPA3 (PMF protects management frames)",
            "Passive monitoring; deauth is useless on 5GHz",
            "DNS lookup; deauth is useless when no clients are connected",
            "Wireshark decryption; deauth is useless on enterprise networks"
        ],
        "answer": 0,
        "explain": "mdk3 brute-forces SSIDs: 'mdk3 wlan0mon p -b u -c 1 -t <BSSID>'. Deauth doesn't work on WPA3 because PMF (802.11w) protects management frames."
    },
    {
        "q": "How do you bypass MAC filtering when spoofing causes a collision with the legitimate client?",
        "options": [
            "Use a random MAC instead of the client's",
            "Deauth the legitimate client first, or spoof a 2.4GHz client's MAC on the 5GHz band",
            "Change the spoofed MAC by one byte",
            "Disable the client's WiFi remotely"
        ],
        "answer": 1,
        "explain": "Two devices with the same MAC can't coexist. Solutions: deauth the real client, or use '--band a' to find a 2.4GHz client's MAC and spoof it on 5GHz."
    },
    {
        "q": "What tool generates default WPS PINs from a BSSID?",
        "options": [
            "reaver --genpin",
            "wpspin -A <BSSID>",
            "wash --default-pins",
            "aircrack-ng --wps-pin"
        ],
        "answer": 1,
        "explain": "wpspin calculates known default PIN algorithms based on the BSSID/MAC. Many vendors use predictable PIN generation."
    },
    {
        "q": "What is genpmk used for, and what's the tradeoff?",
        "options": [
            "Generating WPS PINs; tradeoff is it's slow",
            "Precomputing PMK rainbow tables for a specific SSID; fast cracking but SSID-specific and storage-heavy",
            "Generating packet captures; tradeoff is large file sizes",
            "Creating fake handshakes; tradeoff is they might not work"
        ],
        "answer": 1,
        "explain": "'genpmk -f wordlist -d /tmp/hashtable -s SSID'. Then cowpatty uses it for near-instant cracking — but the table only works for that one SSID."
    },
    {
        "q": "What is the WPA3 SAE brute force tool 'wacker' and why is it different from WPA2 cracking?",
        "options": [
            "It captures PMKID and cracks offline like WPA2",
            "It performs LIVE authentication attempts against the AP — WPA3 resists offline cracking",
            "It exploits a vulnerability in SAE to extract the key",
            "It's the same as hashcat but with WPA3 support"
        ],
        "answer": 1,
        "explain": "WPA3-SAE resists offline PMKID/handshake attacks. Wacker does live auth attempts, no client needed. Much slower but the only option."
    },
    {
        "q": "What is the formula to convert a 2.4GHz WiFi channel number to frequency (for wacker)?",
        "options": [
            "freq = 2400 + (channel * 10)",
            "freq = 2407 + (5 * channel)",
            "freq = 2412 + (channel - 1) * 5",
            "Both B and C give the same result"
        ],
        "answer": 3,
        "explain": "Both formulas work: 2407+(5*ch) and 2412+(ch-1)*5 both give 2412 for ch1, 2417 for ch2, etc."
    },
    {
        "q": "What tools can crack a WPA handshake? Match: cowpatty, aircrack-ng, hashcat, john the ripper.",
        "options": [
            "All four can crack WPA, each needing different input format conversions",
            "Only aircrack-ng and hashcat; others are for WEP only",
            "Only hashcat with GPU; others are too slow",
            "Cowpatty and aircrack-ng for .cap, hashcat and john need format conversion"
        ],
        "answer": 3,
        "explain": "Cowpatty and aircrack-ng read .cap directly. John needs wpapcap2john first. Hashcat needs hcxpcapngtool (-m 22000)."
    },
    {
        "q": "Modern WPS-secured APs lock after failed attempts. What are the typical lockout thresholds?",
        "options": [
            "5 attempts → 30 sec lock, 15 → permanent",
            "3 attempts → 60 sec lock, 10 → 365 days lock",
            "10 attempts → 5 min lock, 20 → 24 hour lock",
            "No lockout, just rate limiting"
        ],
        "answer": 1,
        "explain": "Recent vendors: 3 wrong attempts → 60 sec lock, 10 wrong → 365 days lock. Reaver flags like -L (ignore locks) and -d (delay) help work around this."
    },
    {
        "q": "Netgear default WiFi password pattern is:",
        "options": [
            "8 random alphanumeric characters",
            "{adjective}{noun}{3 digits} like 'sleeksalamander113'",
            "Serial number last 8 characters",
            "MAC address reversed"
        ],
        "answer": 1,
        "explain": "Netgear uses {adjective}{noun}{3digits}. Tools like NPCinator.py generate wordlists based on this pattern. Always check vendor defaults before brute-forcing."
    },
]


def run_quiz():
    print("=" * 65)
    print("  WiFi HACKING QUIZ 3: WPA, WPS & Advanced Techniques")
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
        print("\n  Perfect score! WPA/WPS mastered.")
    print()


if __name__ == "__main__":
    run_quiz()

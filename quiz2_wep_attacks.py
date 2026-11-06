#!/usr/bin/env python3
"""WiFi Hacking Quiz 2: WEP Encryption & Attacks"""

import random

QUESTIONS = [
    {
        "q": "WEP uses a 24-bit IV. How many unique IV values are possible, and roughly how many packets before a 50% collision chance?",
        "options": [
            "16,777,216 unique; ~5,000 packets for 50% collision (birthday paradox)",
            "16,777,216 unique; ~8 million packets for 50% collision",
            "65,536 unique; ~256 packets for 50% collision",
            "4,294,967,296 unique; ~65,000 packets for 50% collision"
        ],
        "answer": 0,
        "explain": "24 bits = 2^24 = 16,777,216 IVs. Birthday paradox gives ~50% collision after only ~5,000 packets — catastrophically small."
    },
    {
        "q": "What does '128-bit WEP' actually mean in terms of key and IV sizes?",
        "options": [
            "128-bit key + 24-bit IV = 152 total bits",
            "104-bit key + 24-bit IV = 128 total bits",
            "128-bit key + 128-bit IV = 256 total bits",
            "64-bit key + 64-bit IV = 128 total bits"
        ],
        "answer": 1,
        "explain": "Marketing lie: '128-bit WEP' = 104-bit key + 24-bit IV. The IV is always 24 bits regardless of the advertised key length."
    },
    {
        "q": "What stream cipher does WEP use, and what are its two components?",
        "options": [
            "AES with CBC and CTR modes",
            "RC4 with KSA (Key Scheduling Algorithm) and PRGA (Pseudo Random Generation Algorithm)",
            "ChaCha20 with key expansion and block function",
            "DES with Feistel network and S-boxes"
        ],
        "answer": 1,
        "explain": "RC4 (Ron Rivest, 1987) is a symmetric stream cipher. KSA initializes the state table with key+IV, PRGA produces the keystream XORed with plaintext."
    },
    {
        "q": "Why is CRC32 a fatal weakness in WEP?",
        "options": [
            "It's too slow and creates a bottleneck",
            "It uses a secret key that can be brute-forced",
            "It's linear: CRC(A⊕B) = CRC(A)⊕CRC(B), enabling bit-flip attacks without knowing the key",
            "It only checks the header, not the payload"
        ],
        "answer": 2,
        "explain": "CRC32 is error-detection only, not cryptographic. Its linearity lets attackers modify ciphertext and recalculate a valid ICV without the key."
    },
    {
        "q": "What is the WEP seed, and how is it constructed?",
        "options": [
            "Seed = HMAC(WEP key, IV)",
            "Seed = IV (24 bits) || WEP key (40 or 104 bits), concatenated",
            "Seed = SHA1(IV + WEP key)",
            "Seed = WEP key XOR IV, padded to 128 bits"
        ],
        "answer": 1,
        "explain": "The seed is simply IV concatenated with the WEP key. The IV is sent in plaintext in the packet header — a critical flaw."
    },
    {
        "q": "What is the ARP Request Replay Attack and which aireplay-ng mode is it?",
        "options": [
            "Mode -5: captures and replays any data packet to generate IVs",
            "Mode -3: captures an ARP packet and replays it, each AP response uses a new IV",
            "Mode -4: forges ARP packets from scratch and floods the network",
            "Mode -2: intercepts ARP replies and modifies them"
        ],
        "answer": 1,
        "explain": "Mode -3 replays captured ARP requests. Each replay triggers a new AP response with a fresh IV, rapidly generating the IVs needed for cracking."
    },
    {
        "q": "The Fragmentation Attack recovers PRGA keystream. How does it get the initial 8 known bytes?",
        "options": [
            "By brute-forcing the first 8 bytes of the key",
            "The LLC/SNAP header's first 7 bytes are always the same, giving 8 bytes of known plaintext",
            "By capturing the IV which is always 8 bytes",
            "By deauthenticating a client and capturing the handshake"
        ],
        "answer": 1,
        "explain": "LLC/SNAP header bytes are predictable. Knowing 8 bytes of plaintext → derive 8 bytes of PRGA keystream. Goal: recover 1500 bytes to forge any packet."
    },
    {
        "q": "After getting a .xor file from fragmentation or chopchop, what tool forges an ARP packet for injection?",
        "options": [
            "aireplay-ng -2",
            "aircrack-ng --forge",
            "packetforge-ng",
            "scapy"
        ],
        "answer": 2,
        "explain": "packetforge-ng creates packets from PRGA: 'packetforge-ng -0 -a <AP> -h <STA> -k <dest_IP> -l <src_IP> -y <xor_file> -w forged.cap'"
    },
    {
        "q": "How does the KoreK ChopChop attack decrypt a packet without the key?",
        "options": [
            "It brute-forces each possible key byte by trying all 256 values against the AP",
            "It removes the last byte, guesses its value (0-255), sends the modified packet — AP drop = wrong, AP accept = correct",
            "It uses a rainbow table of precomputed CRC32 values",
            "It replays the packet with different IVs until a weak IV appears"
        ],
        "answer": 1,
        "explain": "ChopChop (mode -4) truncates one byte at a time, using the AP as an oracle. Correct guess = AP processes it. Repeats byte by byte, recovering PRGA."
    },
    {
        "q": "How do you attack a WEP AP that has NO connected clients?",
        "options": [
            "Wait for a client to connect",
            "Fake authentication (-1) to associate, then fragmentation or chopchop",
            "Use a brute force attack on the key directly",
            "Use mdk3 to flood the AP until it reveals the key"
        ],
        "answer": 1,
        "explain": "Fake auth (-1) associates your card with the AP. Then chopchop (-4) or fragmentation (-5) to get PRGA, forge packets, inject, and crack."
    },
    {
        "q": "What does the fake authentication command look like?\n'aireplay-ng -1 1000 -o 1 -q 5 -e SSID -a BSSID -h OUR_MAC wlan0mon'\nWhat do -o 1 and -q 5 mean?",
        "options": [
            "-o 1 = output format, -q 5 = quiet after 5 attempts",
            "-o 1 = one packet at a time, -q 5 = keep-alive every 5 seconds",
            "-o 1 = open auth mode, -q 5 = quality threshold",
            "-o 1 = one retry, -q 5 = quit after 5 failures"
        ],
        "answer": 1,
        "explain": "-o 1 sends one packet at a time. -q 5 sends keep-alive packets every 5 seconds. 1000 is the reassociation interval."
    },
    {
        "q": "What is the Cafe Latte attack?",
        "options": [
            "A WPA attack that targets coffee shop open networks",
            "A WEP attack that targets clients directly using a fake AP, capturing and replaying ARP packets",
            "A man-in-the-middle attack between client and AP",
            "A social engineering attack at public venues"
        ],
        "answer": 1,
        "explain": "Cafe Latte (mode -6) creates a fake AP with airbase-ng, deauths the client to reconnect to it, then captures/replays ARP for IV generation."
    },
    {
        "q": "What tool creates the fake AP in a Cafe Latte attack?",
        "options": [
            "hostapd",
            "hostapd-mana",
            "airbase-ng",
            "aireplay-ng"
        ],
        "answer": 2,
        "explain": "airbase-ng: 'airbase-ng -c 1 -a <BSSID> -e \"SSID\" wlan0mon -W 1 -L'. The -L flag enables Cafe Latte mode."
    },
    {
        "q": "The FMS attack (2001) exploits what specific weakness in WEP?",
        "options": [
            "Predictable CRC32 checksums",
            "Certain 'weak IVs' that leak key info through the RC4 KSA process",
            "The reuse of the same WEP key across all frames",
            "Buffer overflows in the WEP implementation"
        ],
        "answer": 1,
        "explain": "FMS (Fluhrer, Mantin, Shamir) found that certain IV values create 'weak IVs' where RC4's KSA leaks statistical info about key bytes."
    },
    {
        "q": "What improvement did the PTW attack bring over FMS?",
        "options": [
            "It works without capturing any IVs",
            "It reduced the number of packets needed to tens of thousands, cracking in under a minute",
            "It can crack WPA2 as well as WEP",
            "It doesn't require monitor mode"
        ],
        "answer": 1,
        "explain": "PTW (Pyshkin, Tews, Weinmann) attack needs far fewer packets than FMS. Can crack WEP in under a minute with enough traffic."
    },
    {
        "q": "Why doesn't increasing WEP key size (e.g., 256-bit) fix the vulnerability?",
        "options": [
            "RC4 can't handle keys larger than 128 bits",
            "The IV is always 24 bits regardless of key size — the fundamental weakness remains",
            "Longer keys make the CRC32 weaker",
            "Hardware can't process keys that large"
        ],
        "answer": 1,
        "explain": "The 24-bit IV is the core problem. Even with a 256-bit key, you still have only 16.7M possible IVs and the same collision/weak-IV issues."
    },
    {
        "q": "In the fragmentation attack workflow, after getting the .xor file and forging ARP, how do you inject it?",
        "options": [
            "aireplay-ng -3 (ARP replay mode)",
            "aireplay-ng -2 (interactive packet replay) with the forged .cap",
            "aireplay-ng -5 (fragmentation mode again)",
            "airbase-ng with the forged packet"
        ],
        "answer": 1,
        "explain": "aireplay-ng -2 is interactive packet replay. You feed it the forged ARP .cap file to inject, generating new IVs for cracking."
    },
    {
        "q": "What aircrack-ng flag uses the Korek statistical method for WEP cracking?",
        "options": [
            "-P (PTW method)",
            "-K",
            "-F (FMS method)",
            "--korek"
        ],
        "answer": 1,
        "explain": "'aircrack-ng -K HTB.ivs' uses the Korek method. Without -K, aircrack-ng uses the PTW method by default."
    },
    {
        "q": "What are the two WEP authentication types?",
        "options": [
            "WPA-PSK and WPA-Enterprise",
            "Certificate-based and token-based",
            "Open System (no credentials for encryption) and Shared Key (challenge-response)",
            "Pre-shared key and RADIUS"
        ],
        "answer": 2,
        "explain": "Open System doesn't verify credentials before encryption. Shared Key uses challenge-response (AP sends challenge → client encrypts it → AP verifies)."
    },
    {
        "q": "How many terminals do you need running simultaneously for a Cafe Latte attack?",
        "options": [
            "2 (fake AP + crack)",
            "3 (airodump + fake AP + deauth)",
            "4 (airodump + cafe latte listener + fake AP + deauth)",
            "5 (airodump + fake AP + deauth + replay + crack)"
        ],
        "answer": 2,
        "explain": "Four terminals: airodump-ng for capture, cafe latte packet listener, airbase-ng fake AP, and aireplay-ng for deauth."
    },
]


def run_quiz():
    print("=" * 65)
    print("  WiFi HACKING QUIZ 2: WEP Encryption & Attacks")
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
        print("\n  Perfect score! WEP has no secrets from you.")
    print()


if __name__ == "__main__":
    run_quiz()

# WiFi Hacking — Penetration Testing Notes

A personal knowledge base of Wi-Fi (802.11) penetration-testing notes, techniques, and
tool references. Written and maintained as an [Obsidian](https://obsidian.md) vault, so
internal `[[wiki-links]]` resolve automatically inside Obsidian and render as plain text
elsewhere.

> ⚠️ **Authorized use only.** These notes exist for learning and for authorized security
> work — your own lab, a CTF, or an engagement you have **written permission** to test.
> Attacking networks you don't own or lack explicit authorization to test is illegal in
> most jurisdictions. You are responsible for how you use this material.

---

## 📂 Contents

### Fundamentals
Core 802.11 theory needed before any practical attack.

| Note | Topic |
|------|-------|
| [802.11 Frames and Types](Fundamentals/802.11%20Frames%20and%20Types.md) | MAC frame structure; management / control / data frames and sub-types |
| [Wi-Fi Interfaces](Fundamentals/Wi-Fi%20Interfaces.md) | Wireless adapters and interface naming |
| [Interface Modes](Fundamentals/Interface%20Modes.md) | Managed vs. monitor mode and how to switch |
| [Authentication Methods](Fundamentals/Authentication%20Methods.md) | Open, WEP, WPA/WPA2/WPA3 authentication |
| [WEP IV](Fundamentals/WEP%20IV.md) | WEP initialization vectors and why WEP is broken |
| [Wi-Fi Penetration Testing Basics Overview](Fundamentals/Wi-Fi%20Penetration%20Testing%20Basics%20Overview.md) | High-level methodology and workflow |

### Aircrack-ng Suite
Reference notes for each tool in the [Aircrack-ng](https://www.aircrack-ng.org/) suite.

| Tool | Purpose |
|------|---------|
| [Introduction to Aircrack-ng](Fundamentals/Introduction%20to%20Aircrack-ng.md) | Overview of the suite |
| [Airmon-ng](Fundamentals/Aircrack-ng/Airmon-ng.md) | Enable/disable monitor mode |
| [Airodump-ng](Fundamentals/Aircrack-ng/Airodump-ng.md) | Capture packets and discover networks/clients |
| [Aireplay-ng](Fundamentals/Aircrack-ng/Aireplay-ng.md) | Inject frames (deauth, replay, etc.) |
| [Aircrack-ng](Fundamentals/Aircrack-ng/Aircrack-ng.md) | Crack WEP/WPA keys from captures |
| [Airdecap-ng](Fundamentals/Aircrack-ng/Airdecap-ng.md) | Decrypt captured traffic |
| [Airgraph-ng](Fundamentals/Aircrack-ng/Airgraph-ng.md) | Visualize client/AP relationships |

### Techniques
Hands-on attack and recon write-ups.

| Note | Technique |
|------|-----------|
| [Finding Hidden SSIDs](Finding%20Hidden%20SSIDs.md) | Reveal hidden networks via passive monitoring and deauth |
| [Bypassing MAC Filtering](Bypassing%20Mac%20Filtering.md) | Spoof an allowed MAC to defeat MAC-based access control |

---

## 🧰 Typical Toolkit

- **[Aircrack-ng suite](https://www.aircrack-ng.org/)** — monitor mode, capture, injection, cracking
- **A monitor-mode-capable Wi-Fi adapter** (chipset with `nl80211` / injection support)
- **[Kali Linux](https://www.kali.org/)** (or any distro with the wireless stack installed)
- Supporting tools as needed: `iw`, `macchanger`, `wireshark`, `hashcat`

## 🚀 Getting Started

1. Open this folder as a vault in **Obsidian** to browse notes with working links and graph view.
2. Or read any `.md` file directly in a text editor / on GitHub.
3. Start with **[Wi-Fi Penetration Testing Basics Overview](Fundamentals/Wi-Fi%20Penetration%20Testing%20Basics%20Overview.md)**, then the rest of *Fundamentals*, before the *Techniques* notes.

## 🗺️ Suggested Learning Path

```
Fundamentals (theory)
  └─ 802.11 Frames → Interfaces → Interface Modes → Authentication Methods → WEP IV
        │
        ▼
Aircrack-ng Suite (tooling)
  └─ Airmon → Airodump → Aireplay → Aircrack → Airdecap / Airgraph
        │
        ▼
Techniques (practice, in a lab)
  └─ Finding Hidden SSIDs → Bypassing MAC Filtering
```

## 🤝 Notes

This is a living set of personal study notes — expect them to grow and change. If you fork
or reuse them, keep the authorized-use principle above intact.

## 📄 License

Personal study notes. No warranty. Use at your own risk and within the law.

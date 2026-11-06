
## Overview
In WPA-Enterprise (802.1X/EAP) networks, the authentication server sends its TLS certificate to the client in cleartext during the EAP-TLS/PEAP handshake. Anyone who captures this exchange can read the certificate without authenticating.

## Information Exposed
- Common Name (CN)
- Organization and organizational unit
- Email address
- Issuing CA details
- Validity period
- Public key and signature algorithm

## Procedure
1. Capture or open a pcap containing the EAP handshake.
2. Filter for the TLS Certificate message:
   `tls.handshake.type == 11`
3. Expand the packet:
   `Transport Layer Security > Handshake Protocol: Certificate > Certificates > signedCertificate`
4. Inspect the `subject` (server) and `issuer` (CA) fields.

## CLI Alternative
    tshark -r capture.pcap -Y "tls.handshake.type==11" -V | grep -i email

Or export the certificate as DER and parse it:

    openssl x509 -inform DER -in cert.der -text -noout

## Key Distinction
| Field    | Identifies                            |
|----------|---------------------------------------|
| subject  | The server the certificate belongs to |
| issuer   | The CA that signed the certificate    |

## Security Relevance
- Certificate details help fingerprint the target network and its PKI.
- They can be used to build a convincing rogue AP (evil twin) with similar certificate attributes.
- Clients that do not validate the server certificate are vulnerable to credential capture.

## Mitigation
- Enforce server certificate validation on all clients.
- Pin the trusted CA and the server name in the supplicant configuration.
- Avoid placing sensitive details (personal emails, internal hostnames) in certificate fields.
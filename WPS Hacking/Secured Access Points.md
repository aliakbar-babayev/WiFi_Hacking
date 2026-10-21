
Traditionally, online brute-forcing attempts have been utilized in retrieving the WPS PIN and WPA-PSK. However, in recent years, manufacturers have become wiser to these attacks. As such, locking has been utilized to prevent these traditional bruteforcing techniques. The most recent vendors only allow up to 3 incorrect attempts. After each incorrect attempt, the AP will lock for 60 seconds. After 10 incorrect attempts, the AP will lock for 365 days.

In some cases, vendors might have not implemented strict lock mechanisms, allowing us to continue bruteforcing using Reaver. The tool can be fine-tuned with additional advanced switches to optimize the bruteforce process, for example:

|**Option**|**Description**|
|---|---|
|`-L, --ignore-locks`|Ignore locked state reported by the target AP|
|`-N, --no-nacks`|Do not send NACK messages when out of order packets are received|
|`-d, --delay=<seconds>`|Set the delay between pin attempts 1|
|`-T, --m57-timeout=<seconds>`|Set the M5/M7 timeout period 0.40|
|`-r, --recurring-delay=<x:y>`|Sleep for y seconds every x pin attempts|

This leads us to ask the following questions when employing these brute-forcing techniques:

- Will the access point lock after 3 incorrect attempts?
- How long does the access point stay locked? (Different vendors have different locking time.)
- Would PIN generation algorithms allow us to refine the total amount of guesses? (Covered in the next section.)

If the access point (AP) locks after three incorrect attempts, using PIN generation algorithms to narrow down the total number of guesses and create a custom wordlist can be beneficial. However, in some cases, we might get lucky and find the correct PIN within the first 10 bruteforce attempts, before the AP locks indefinitely. Gathering information on these questions through research and enumeration allows us to craft better attacks towards WPS services for access points. The better technique that we utilize, the lower our chances are of failure when attempting to retrieve the PSK through WPS.


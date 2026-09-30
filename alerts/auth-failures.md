# Alert: authentication failures (possible brute force)

## Where to build it
**System → Events → Event Definitions → Create Event Definition**
(Type: Filter & Aggregation.)

## Configuration

| Setting | Value |
|---|---|
| Title | `auth-failures-bruteforce` |
| Filter (search query) | `application_name:sshd AND message:"Failed password"` |
| Search within the last | 5 minutes |
| Execute search every | 5 minutes |
| Aggregation | `count() > 10` |
| Group by | `source` |
| Event fields | `source`, `message` (include in the event) |

## Notification text (suggestion)

```
Possible brute-force logins on ${event.fields.source}: more than 10
failed SSH passwords in 5 minutes. Check whether the source IPs are
known scanners or internal hosts, then block / rotate credentials.
```

## Threshold rationale
A human mistypes a password a few times; 10+ failures in 5 minutes from
one host is automation. The `Group by source` keeps one noisy host from
masking a quieter attack on another. Tune the count down (5) for
internet-facing bastions, up (25) for hosts behind SSO where interactive
SSH should be rare.

## What "real" looks like vs noise
Real: failures spread across many usernames (`admin`, `root`, `test`)
from one external IP = password guessing. Noise: one user, one IP,
three failures at 9 AM = someone forgot their password.

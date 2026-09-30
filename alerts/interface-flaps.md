# Alert: interface flapping

## Where to build it
**System → Events → Event Definitions → Create Event Definition**
(Type: Filter & Aggregation.)

## Configuration

| Setting | Value |
|---|---|
| Title | `interface-flapping` |
| Filter (search query) | `message:"%LINEPROTO-5-UPDOWN" OR message:"%LINK-3-UPDOWN"` |
| Search within the last | 10 minutes |
| Execute search every | 10 minutes |
| Aggregation | `count() > 4` |
| Group by | `source` |

## Notification text (suggestion)

```
Interface flapping on ${event.fields.source}: ${event.fields.count}
up/down transitions in 10 minutes. Check the physical layer (cable,
SFP, patch panel) and the peer device before assuming a config issue.
```

## Threshold rationale
A single up/down pair happens on every planned change — the *rate* is
the signal. More than 4 transitions in 10 minutes from one device means
the link cannot hold state and will take user traffic with it when it
finally dies. Start at 4 and raise it only if a specific device has a
known-chatty peer.

## What "real" looks like vs noise
Real: the same interface alternating down/up every 90 seconds for an
hour = failing optic or marginal cable. Noise: one down/up pair during
a maintenance window = someone reseated a cable on purpose.

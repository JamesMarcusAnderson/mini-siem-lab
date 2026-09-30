# Alert: device restarts (unscheduled reboot)

## Where to build it
**System → Events → Event Definitions → Create Event Definition**
(Type: Filter & Aggregation.)

## Configuration

| Setting | Value |
|---|---|
| Title | `device-restart-detected` |
| Filter (search query) | `message:"%SYS-5-RESTART" OR message:"System restarted" OR (application_name:systemd AND message:"Startup finished")` |
| Search within the last | 15 minutes |
| Execute search every | 15 minutes |
| Aggregation | `count() > 0` |
| Group by | `source` |

## Notification text (suggestion)

```
${event.fields.source} rebooted at ${event.timestamp}. If this was not a
scheduled maintenance window, treat as an incident: check power, crash
logs, and watchdog configuration.
```

## Threshold rationale
Any reboot is the signal — the threshold is 1. The 15-minute window
keeps the event definition cheap (it only runs 4×/hour) while still
catching the boot. Grouping by `source` gives you one event per host
instead of one event per boot line.

## What "real" looks like vs noise
Real: a core switch rebooting at 03:12 with no change ticket = incident.
Noise: your lab VM rebooting when you ran `apt upgrade` = expected.
Suppress with a maintenance-window schedule in Graylog (Events →
the definition's scheduling) for known change windows.

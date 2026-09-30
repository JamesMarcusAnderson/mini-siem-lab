# Alert: service errors (severity-driven)

## Where to build it
**System → Events → Event Definitions → Create Event Definition**
(Type: Filter & Aggregation.)

## Configuration

| Setting | Value |
|---|---|
| Title | `service-errors-spike` |
| Filter (search query) | `level:[0 TO 3]` |
| Search within the last | 5 minutes |
| Execute search every | 5 minutes |
| Aggregation | `count() > 25` |
| Group by | `source`, `application_name` |

## Notification text (suggestion)

```
Error spike: ${event.fields.application_name} on ${event.fields.source}
logged 25+ severity 0-3 messages in 5 minutes.
Open the service-errors saved search scoped to that host and check
whether it is one repeated error or many different ones.
```

## Threshold rationale
Severity 0–3 (emerg/alert/crit/err) should be rare on a healthy host,
so the threshold is a *spike* detector, not a presence detector. 25 per
5 minutes is a starting point: a quiet host can use 5, a busy web tier
may need 100. Grouping by `source` + `application_name` tells you
*which service on which box* without opening the search.

## What "real" looks like vs noise
Real: 200 `mysqld` errors in 3 minutes all saying `Can't connect` =
the database is down. Noise: one `nginx` emerg at deploy time =
someone fat-fingered a config and fixed it. Correlate with the
device-restarts and interface-flaps alerts before paging anyone —
an error storm right after a reboot is a symptom, not a second incident.

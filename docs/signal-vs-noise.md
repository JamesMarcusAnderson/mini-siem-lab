# Signal vs noise: how to tell a real incident from log chatter

A SIEM that pages on every error is a SIEM everyone mutes. The skill is
not writing alerts — it's writing alerts that stay quiet until something
is actually wrong. These are the techniques working NOC/SOC analysts use.

## 1. Baseline first, alert second

Before setting a threshold, watch the metric for a week. If a web server
normally logs 40 nginx errors per hour at peak, an alert at "more than
50/hour" will fire every busy afternoon. Set the threshold at 2–3× the
normal peak, not at a round number that felt right.

In Graylog: build the aggregation widget for the query, look at the
last 7 days, and pick the threshold from the data.

## 2. Rate beats presence

Almost nothing should alert on a single log line. One failed login is
a typo; fifty in a minute is a brute force. One interface flap is a
cable reseat; six in ten minutes is a dying optic. Every alert in this
repo's `alerts/` directory is a *rate* (`count() > N in T minutes`),
never a *presence* check.

## 3. Correlate across sources before paging

A single alert is a hint; two related alerts are an incident. Before
escalating, check the other three detections:
- Error spike + device restart 2 minutes earlier → the errors are a
  *symptom* of the reboot, not a second incident.
- Auth failures from one IP + the same IP in the firewall logs →
  confirm the attack path.
- Interface flaps on two ends of the same link → it's the link, not
  either device.

## 4. Group by the right field

`count() > 10` across the whole fleet is meaningless — one noisy host
hides a quiet attack on another. Always `Group by source` (and by
`application_name` for service errors) so each host gets its own
budget. An alert that can't name the host is an alert nobody can act on.

## 5. Tune on a schedule, not on frustration

Alert fatigue kills monitoring programs: analysts start ignoring the
console, then miss the real one. Monthly, review which alerts fired and
ask of each: did this page lead to action? If an alert fired 30 times
and never once led to a ticket, raise its threshold or delete it. A
deleted noisy alert is a reliability improvement.

## 6. Separate the layers

- **Noise:** single errors during deploys, one-off flaps during
  maintenance, failed logins at 9 AM from known users.
- **Signal:** error *rates* changing, the *same* failure repeating,
  failures *correlated* across devices, anything happening at 3 AM
  that normally happens at 3 PM.

## 7. Keep a runbook link in every notification

The notification templates in `alerts/` tell the responder what to check
first. An alert without a next step is just anxiety with a timestamp.

# Saved search: service errors

## What it catches
Applications and daemons reporting real errors — HTTP 500s from nginx,
failed systemd units, database connection failures. The `level` field
comes from the syslog severity, so this is severity-driven, not
keyword-guessing.

## Query (Graylog search syntax)

```
level:[0 TO 3]
```

with an optional application filter, e.g.:

```
level:[0 TO 3] AND (application_name:nginx OR application_name:mysqld OR application_name:systemd)
```

## Why this shape
- Syslog severities 0–3 are emerg, alert, crit, err — the levels that
  mean "something is actually broken". Graylog parses the `<PRI>`
  header into the numeric `level` field automatically.
- `level:[0 TO 3]` is a Lucene range query: far more reliable than
  grepping for the word "error", which appears in harmless lines like
  `error_log /var/log/nginx/error.log;`.
- Adding `application_name` scopes it to the services you care about
  and keeps routine kernel warnings out of the view.

## Useful refinements
A message-text companion query catches application errors that arrive
without a proper severity:

```
message:("connection refused" OR "out of memory" OR "segfault" OR "FAILED" OR "Traceback")
AND NOT level:[0 TO 3]
```

If that second query returns a lot, those senders need their syslog
severity fixed — that itself is a finding.

## Save it
Paste the query into **Search**, set the time range, then
**Search actions → Save search** and name it `service-errors`.

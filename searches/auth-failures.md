# Saved search: authentication failures

## What it catches
Repeated failed logins — brute-force password guessing, credential
stuffing, or a misconfigured service account hammering the wrong
password. This is the single most common thing a NOC/SOC watches.

## Query (Graylog search syntax)

```
(application_name:sshd OR application_name:login OR application_name:su OR application_name:sudo)
AND
(message:"Failed password" OR message:"authentication failure" OR message:"Invalid user" OR message:"FAILED LOGIN")
```

## Why this shape
- `application_name` narrows to the daemons that actually authenticate,
  instead of matching the word "failed" across every log line on the box.
- The `message:` phrases are the literal strings Linux PAM/sshd emit:
  `Failed password for invalid user admin from 203.0.2.10 port 52344 ssh2`,
  `pam_unix(sshd:auth): authentication failure`, etc.
- Parentheses matter: in Graylog (Lucene syntax) `AND` binds tighter
  than `OR`, so the grouping keeps the logic correct.

## Useful refinements
Group an aggregation by `source` to find the *target* being attacked,
or by the source IP inside `message` to find the *attacker*:

```
# top targeted hosts (use with a "Group by source" aggregation widget)
application_name:sshd AND message:"Failed password"
```

## Save it
Paste the query into **Search**, set the time range, then
**Search actions → Save search** and name it `auth-failures`.

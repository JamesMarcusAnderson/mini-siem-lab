# mini-siem-lab

A NOC drowns in logs. Every switch, server, and firewall emits thousands
of lines a day, and the difference between "we caught the outage at
03:12" and "the customer told us at 09:00" is whether those logs can
answer questions. This lab shows how: collect syslog centrally with
Graylog, write searches that find the four failure patterns every NOC
watches for, alert on *rates* instead of single lines, and know how to
tell a real incident from noise.

## Architecture

```
network devices / linux hosts
        │  syslog (UDP/TCP 1514)
        ▼
  ┌──────────┐
  │ Graylog  │──▶ MongoDB (config) + OpenSearch (log storage)
  └──────────┘
        │
        ├──▶ saved searches: auth failures · restarts · flaps · service errors
        └──▶ event alerts: rate-based thresholds per host
```

## What's in here

| Path | What it is |
|---|---|
| `docker-compose.yml` | Graylog 6.1 + MongoDB 7.0 + OpenSearch 2.15 stack. One command to run. |
| `graylog/inputs.md` | How to launch the Syslog UDP/TCP inputs and forward devices to them. |
| `searches/` | Four saved-search definitions with real Graylog query syntax: authentication failures, device restarts, interface flaps, service errors. |
| `alerts/` | Four event-definition specs (filter, aggregation, threshold, group-by) plus notification text and tuning rationale. |
| `docs/signal-vs-noise.md` | How to separate real incidents from noise: baselining, rate-based alerting, correlation, scheduled tuning. |
| `scripts/send-test-syslog.py` | Generates clearly-marked **synthetic** syslog traffic to exercise the searches and alerts. Standard library only. |

## Setup

```bash
docker compose up -d
# wait ~60s, then open http://127.0.0.1:9000  (admin / admin — change it)
```

1. Follow `graylog/inputs.md` to launch the Syslog UDP input on port 1514.
2. Send test traffic: `python3 scripts/send-test-syslog.py --host 127.0.0.1`
3. In Graylog **Search**, paste any query from `searches/` and watch it match.
4. Build the event definitions from `alerts/` and re-run the generator to see them fire.

## What a reviewer will see

- A working, version-coherent Graylog stack defined as code.
- Detection logic for the four patterns NOC hiring managers ask about:
  brute-force logins, unscheduled reboots, flapping interfaces, and
  application error spikes — each with a query, an alert threshold, and
  a written rationale for the threshold.
- An explicit signal-vs-noise methodology: baselining, correlation,
  and scheduled alert tuning — the part of SIEM work that separates an
  operator from someone who just installed a dashboard.

## Scope

Lab environment with **synthetic test logs only** — every generated line
is tagged `[TEST-NOT-REAL]` and uses RFC 5737 documentation IP space.
No production data, no real incident data, no third-party systems.

## Keywords

SIEM · syslog · Graylog · OpenSearch · log analysis · alerting ·
event correlation · incident detection · threshold tuning · NOC ·
network monitoring

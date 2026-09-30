# Configuring Syslog inputs in Graylog

Graylog collects logs through **inputs** — listeners bound to a port and
protocol. For this lab we use the built-in Syslog inputs on port 1514
(non-privileged; the Graylog container runs as a non-root user, so it
cannot bind port 514).

## 1. Syslog UDP input

1. Log in to the web UI at `http://127.0.0.1:9000` (admin / admin).
2. Go to **System → Inputs**.
3. In the **Select input** dropdown choose **Syslog UDP**, then click
   **Launch new input**.
4. Fill in:
   - **Title:** `Syslog UDP`
   - **Bind address:** `0.0.0.0`
   - **Port:** `1514`
   - **Receive Buffer Size:** `262144`
   - **Allow overriding date:** checked (lets the sender's timestamp win)
   - **Store full message:** checked (keeps the raw line in `full_message`)
5. Click **Launch input**. The input appears in the list with a green
   **RUNNING** state.

## 2. Syslog TCP input

Repeat the same steps, but choose **Syslog TCP** and title it
`Syslog TCP`. Use TCP when you cannot afford to lose messages
(UDP has no delivery guarantee).

## 3. Verify messages are arriving

With the inputs running, send the synthetic test traffic:

```bash
python3 scripts/send-test-syslog.py --host 127.0.0.1
```

Then in Graylog go to **Search** and run `*` over "Search in the last
5 minutes" — you should see messages with `source` set to the sending
host and `application_name` values like `sshd`, `kernel`, `nginx`.

If nothing arrives:
- `docker compose ps` — all three services must be `Up`.
- On the Inputs page the input must show RUNNING (not just configured).
- From the host: `nc -u 127.0.0.1 1514` then type a line — it should
  appear in Search within seconds.
- Check for a local firewall blocking UDP/TCP 1514.

## 4. Forwarding real device logs (reference)

On a Linux box with rsyslog, forwarding everything to this lab is one
line in `/etc/rsyslog.d/50-graylog.conf`:

```
*.* @127.0.0.1:1514      # UDP
*.* @@127.0.0.1:1514     # TCP (note the double @)
```

then `systemctl restart rsyslog`.

On Cisco IOS:

```
logging host 192.0.2.50 transport udp port 1514
logging trap informational
```

On Juniper Junos:

```
set system syslog host 192.0.2.50 any any
set system syslog host 192.0.2.50 port 1514
```

Only point devices you own (or are authorized to monitor) at this lab.

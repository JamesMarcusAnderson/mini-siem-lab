#!/usr/bin/env python3
"""Send SYNTHETIC test syslog traffic to the lab Graylog instance.

This generates clearly fake log lines (TEST-NOT-REAL markers, example IP
space from RFC 5737) so you can exercise the saved searches in searches/
and the alert definitions in alerts/ without any production data.

Usage:
    python3 scripts/send-test-syslog.py --host 127.0.0.1 [--port 1514] [--count 50]

Requires: the Graylog Syslog UDP input running on <host>:<port>
(see graylog/inputs.md). Python 3, standard library only.
"""
import argparse
import datetime
import random
import socket
import sys
import time

# RFC 3164: <PRI>TIMESTAMP HOSTNAME TAG: MESSAGE
# PRI = facility * 8 + severity
FACILITIES = {
    "kern": 0, "user": 1, "daemon": 3, "auth": 4,
    "authpriv": 10, "local0": 16,
}
SEVERITIES = {
    "emerg": 0, "alert": 1, "crit": 2, "err": 3,
    "warning": 4, "notice": 5, "info": 6, "debug": 7,
}


def pri(facility: str, severity: str) -> int:
    return FACILITIES[facility] * 8 + SEVERITIES[severity]


def stamp() -> str:
    # RFC 3164 timestamp: "Mmm dd hh:mm:ss"
    return datetime.datetime.now().strftime("%b %d %H:%M:%S")


# (facility, severity, hostname, tag, message) — all synthetic.
TEMPLATES = [
    # --- authentication failures: drives searches/auth-failures.md + alerts/auth-failures.md
    ("authpriv", "warning", "web01", "sshd[2142]",
     "Failed password for invalid user admin from 203.0.113.10 port 52344 ssh2 [TEST-NOT-REAL]"),
    ("authpriv", "warning", "web01", "sshd[2142]",
     "Failed password for root from 203.0.113.10 port 52345 ssh2 [TEST-NOT-REAL]"),
    ("authpriv", "info", "web01", "sshd[2142]",
     "pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=203.0.113.10 [TEST-NOT-REAL]"),
    # --- device restarts: drives searches/device-restarts.md + alerts/device-restarts.md
    ("daemon", "notice", "switch01", "%SYS-5-RESTART",
     "System restarted -- [TEST-NOT-REAL]"),
    ("daemon", "info", "web01", "systemd[1]",
     "Startup finished in 2.134s (kernel) + 4.882s (userspace) = 7.016s [TEST-NOT-REAL]"),
    ("kern", "info", "web01", "kernel",
     "Booting Linux on physical CPU 0x0 [TEST-NOT-REAL]"),
    # --- interface flaps: drives searches/interface-flaps.md + alerts/interface-flaps.md
    ("local0", "warning", "switch01", "%LINEPROTO-5-UPDOWN",
     "Line protocol on Interface GigabitEthernet0/1, changed state to down [TEST-NOT-REAL]"),
    ("local0", "warning", "switch01", "%LINEPROTO-5-UPDOWN",
     "Line protocol on Interface GigabitEthernet0/1, changed state to up [TEST-NOT-REAL]"),
    ("local0", "err", "switch01", "%LINK-3-UPDOWN",
     "Interface GigabitEthernet0/1, changed state to down [TEST-NOT-REAL]"),
    ("kern", "warning", "web01", "kernel",
     "igb 0000:01:00.0 eth0: NIC Link is Down [TEST-NOT-REAL]"),
    # --- service errors: drives searches/service-errors.md + alerts/service-errors.md
    ("daemon", "err", "web01", "nginx[881]",
     "2026/09/30 12:00:00 [error] 881#881: *42 upstream timed out (110: Connection timed out) [TEST-NOT-REAL]"),
    ("daemon", "crit", "db01", "mysqld[402]",
     "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2) [TEST-NOT-REAL]"),
    ("daemon", "err", "web01", "systemd[1]",
     "Failed to start Test Web Service. [TEST-NOT-REAL]"),
    # --- benign background chatter (so the stream looks like a real syslog feed)
    ("daemon", "info", "web01", "systemd[1]",
     "Starting Daily apt download activities... [TEST-NOT-REAL]"),
    ("kern", "info", "web01", "kernel",
     "UFW ALLOW IN=eth0 OUT= SRC=198.51.100.7 DST=192.0.2.10 [TEST-NOT-REAL]"),
]


def build_message(tpl) -> bytes:
    facility, severity, host, tag, msg = tpl
    line = f"<{pri(facility, severity)}>{stamp()} {host} {tag}: {msg}"
    return line.encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1", help="Graylog host")
    ap.add_argument("--port", type=int, default=1514, help="Syslog UDP port")
    ap.add_argument("--count", type=int, default=50,
                    help="total messages to send")
    ap.add_argument("--delay", type=float, default=0.2,
                    help="seconds between messages")
    args = ap.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for i in range(args.count):
            tpl = random.choice(TEMPLATES)
            sock.sendto(build_message(tpl), (args.host, args.port))
            if args.delay:
                time.sleep(args.delay)
    except OSError as exc:
        print(f"send failed: {exc}", file=sys.stderr)
        return 1
    print(f"sent {args.count} synthetic syslog messages to {args.host}:{args.port} (UDP)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Saved search: device restarts

## What it catches
Unexpected reboots of servers or network gear — crashes, power events,
watchdog resets, or someone reloading a switch at 2 AM. A restart you
didn't schedule is always worth a look.

## Query (Graylog search syntax)

```
(message:"%SYS-5-RESTART" OR message:"System restarted")
OR
(application_name:systemd AND message:"Startup finished")
OR
(application_name:kernel AND message:"Booting Linux")
```

## Why this shape
- `%SYS-5-RESTART: System restarted --` is the literal message Cisco IOS
  emits on reload; matching it catches switch/router reboots with zero
  false positives.
- `systemd ... Startup finished in ...` fires once per Linux boot.
- `kernel ... Booting Linux` catches the kernel ring-buffer start.
- Each clause is a *different device's* way of saying "I just booted",
  OR'd together so one search covers the whole fleet.

## Useful refinements
Exclude planned maintenance windows by adding the window as a NOT
clause, or aggregate `count() by source` to spot a device rebooting
in a loop (more than 2 boots/hour from one host is never normal).

## Save it
Paste the query into **Search**, set the time range, then
**Search actions → Save search** and name it `device-restarts`.

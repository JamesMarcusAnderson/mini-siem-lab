# Saved search: interface flaps

## What it catches
A link bouncing up and down — bad cable, failing SFP, duplex mismatch,
or a peer rebooting. One flap is trivia; a *pattern* of flaps is an
incident in progress.

## Query (Graylog search syntax)

```
message:"%LINEPROTO-5-UPDOWN"
OR
message:"%LINK-3-UPDOWN"
OR
(application_name:kernel AND message:"link" AND (message:"down" OR message:"up"))
```

## Why this shape
- `%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down`
  is the exact Cisco IOS line-protocol message; `%LINK-3-UPDOWN` is its
  link-state sibling. Matching the mnemonics avoids false hits on
  unrelated lines containing the word "interface".
- The kernel clause catches Linux (`igb 0000:01:00.0 eth0: NIC Link is Down`):
  requiring `link` plus `up`/`down` keeps it tight.
- In Lucene syntax `AND` binds tighter than `OR`, so the parenthesised
  kernel clause is evaluated as one unit.

## Useful refinements
Flaps only matter as a *rate*. In a dashboard, use this query with an
aggregation of `count() by source` over 15 minutes — any host with more
than a handful of flaps gets a ticket. See `alerts/interface-flaps.md`.

## Save it
Paste the query into **Search**, set the time range, then
**Search actions → Save search** and name it `interface-flaps`.

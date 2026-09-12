# A day in the life of a three-role project

Three chats — **review**, **build**, **compliance** — share one folder. The human runs the
terminal and makes the decisions. Here is one ordinary afternoon, to show the shape.

## 14:02 — build ships something

Build finishes a feature, verifies it live, bumps the two documents it touched, and writes
one message to its own pane:

```
**LIST ROUTING SHIPPED — c361610 (build -> review, ACTION: review) — 2026-01-14**

- signed-in visitors now land on the docked workshop; signed-out and phone paths unchanged
- behavioural check: a signed-in click on "Build from this list" opens the workshop seeded
- Docs on disk: ARCHITECTURE v1.106. Ask: row sync only.
```

Build does not tell the human. The human opens the folder later and can *see* the message
sitting there, which is the point.

## 14:30 — the human opens the review chat

Review's first motion, unprompted, is the relay pass: it reads all three panes. It finds
build's message, updates the tracker row, then **consumes** — deletes the message from
`from-build.md` and writes a receipt into that file's hidden block, one motion:

```
**RECEIPT rev-2026-01-14-a** — consumed the routing ship; row synced; ARCHITECTURE v1.106
verified on disk. Nothing owed.
```

Note "verified on disk": a docs line in a report is a claim, not a receipt. Review looked.

## 14:31 — review needs a ruling it cannot make

The feature touches how user-pasted text is handled. That is a privacy question, and privacy
is compliance's hat. Review does **not** answer it. It writes to its own pane:

```
**PASTED-TEXT HANDLING — wording needed (review -> compliance, ACTION: compliance) — 2026-01-14**

- users will paste itineraries for a verdict; standing posture is ephemeral, never logged
- PRIVACY.md needs one line saying so. You rule the wording; build's pen writes it.
```

## 15:10 — compliance rules

Compliance reads its panes, consumes review's message, and writes its ruling — addressed to
**build**, because build owns PRIVACY.md — with review named as FYI. One action recipient;
FYI readers act on nothing.

## 15:40 — build reads, and finds a passenger

Build consumes compliance's ruling and writes the line into PRIVACY.md. But the message also
carried a rider: *"review — note the version bump on your tracker."* Build is not review.
So before clearing, build carries that rider forward in its own next message. **Clearing is
destructive; read what you are destroying.**

## 17:00 — the human checks in

Every pane is empty. The human never copied a single message between windows. Their only
role all afternoon was to *decide* — and every chat that needed something from them ended
its reply with a short **Needs you** list, so nothing was buried.

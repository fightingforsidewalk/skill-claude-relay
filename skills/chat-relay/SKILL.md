---
name: chat-relay
description: A file-based mailbox protocol for passing messages between several Claude chats (or any AI assistants) that share one folder of Markdown files — read-and-clear as one motion, receipts, standing notes, fold-forward, and the passenger rule. Use it at the start of every turn in a multi-chat project ("check the relay", "there's a message for you from Build"), when scaffolding a new project's RELAY folder, or before sending or overwriting your own outbox file.
---

# The open-pane relay

Several chats work on one project. Each wears a named hat (say **review**, **build**,
**compliance**) and owns different files. They cannot talk to each other directly, and the
human should never be the courier. So each chat gets **one outbox file** in a shared folder,
and the protocol below turns those files into a mailbox everyone can trust.

The whole thing is plain Markdown. An Obsidian vault is the nicest host — the `%%` markers
hide the meta block in reading view — but nothing depends on it. Any folder that all the
chats can read and write will do.

## The shape of a pane

One file per role: `RELAY/from-review.md`, `RELAY/from-build.md`, `RELAY/from-compliance.md`.
Each chat **writes only its own pane** — with exactly one exception, described under *Consuming*.

```
# FROM BUILD - outbox

Everything between the rules below is an UNREAD message, in plain view on purpose. ...

---

**SHORT TITLE (build -> review, ACTION: review) — 2026-01-14**

- what happened, in one to three lines per item
- what is needed, if anything ("Ask: row sync only", "Ask: rule the wording")

---
%%
**RECEIPT rev-2026-01-14-a** — consumed the message above; recorded where; nothing owed.

PROTOCOL — THE OPEN PANE. (the standing description of the protocol, verbatim)

STANDING NOTES (owner's, preserved verbatim by everyone)
...
%%
```

**Visible, at the top:** a one-line statement of what the pane is, then every unread message
under its own bold heading naming its **one ACTION recipient**. **Hidden, at the foot,
between the two `%%` markers:** the receipt log (newest first), the protocol header, and the
owner's standing notes. An empty visible pane reads `*(no message pending)*` and means
exactly that.

The point is not cosmetic. **A pending message the human can see at a glance makes them a
check on the process; a hidden one makes them someone the chats can quietly fail in front
of.** An earlier version of this protocol hid the whole message inside the comment block.
It was worse in every way.

## The rules

1. **The relay pass is the first motion of every turn, unprompted.** Read every pane before
   doing anything else. Do not wait to be told a message is waiting.
2. **One ACTION recipient per message, always.** Two chats must act → two messages, each under
   its own heading. Readers named as FYI act on nothing, clear nothing, and are owed nothing.
3. **Reading is clearing — one motion, one turn.** A message addressed to you: consume it,
   then DELETE it from the sender's visible pane in the same turn, and write one receipt line
   into that pane's hidden block. A message left visible after you have acted on it will be
   acted on again. A message superseded between your read and your clear dies unread — hence
   one motion.
4. **Consuming is the single exception to single-writer.** You edit another chat's pane only
   to remove the message addressed to you and add your receipt, and you preserve the owner's
   standing notes **verbatim**.
5. **Fold-forward.** Before overwriting your own visible pane, look at it. A still-present
   message is unconsumed and folds forward **in full**. Compress an item only when the
   recipient's own later message has made it moot, and say so. **An ask is never dropped in
   a fold.** If the same message folds forward more than twice, say so in the message.
6. **The passenger rule.** A message can carry a rider for a chat that is not its action
   recipient, and clearing the carrier destroys the rider. Before clearing anything, check
   whether any part of it is addressed to a third chat, and if so carry that part forward in
   your own next message. The fold-forward rule protects your own unconsumed messages; the
   passenger rule protects everyone else's. Both reduce to: **clearing is destructive, so
   read what you are destroying before you destroy it.**
7. **Transport, not record.** Durable facts go to the tracker, the log, or the owning
   document *before* they ride the relay, so a message is always safe to clear.
8. **The human is input, never transport.** They may read any pane whenever they like — that
   is the point of the visible body — and they may paste something when they want to. They
   are never asked to relay, poke, or request a clear.
9. **Receipts are short.** Confirm what you consumed, say where you recorded it, name any ask
   you are returning. Ten lines is a long receipt.

## The delimiter hazard

The hidden block is bounded by two `%%` markers, and `%%` is a **toggle**. Two things follow:

- **Never write the marker inside a visible body.** It would open a block and hide everything
  after it. Refer to it in prose as "the comment markers", and in scripts build it as
  `chr(37) * 2` so it never appears literally in your own source.
- **Balanced syntax is absolute inside the hidden block** — no lone `$`, no unclosed code
  fence, no stray angle-bracket placeholder. An odd dollar sign once opened an inline-math
  span that swallowed a pane's own closing marker. In the visible pane an odd `$` is merely
  cosmetic.

And the general form, which outlives any particular renderer: **asserting that the file has
exactly two markers proves the block is closed, not that any given content sits on the side
of it you intended. Check the side, not the count.**

## Using the script

`scripts/relay.py` does the mechanical parts and refuses the dangerous ones. Every write goes
to a temp file and lands by atomic replace.

```
python3 relay.py init  RELAY --roles review build compliance
python3 relay.py status RELAY
python3 relay.py send  RELAY --from build --to review --title "ROUTING SHIPPED" --body-file msg.md
python3 relay.py consume RELAY --pane build --as review --receipt "consumed the routing ship; recorded on the board; nothing owed."
```

`consume` removes **only** the messages whose ACTION recipient is the role you pass; anything
addressed to someone else stays in the pane untouched (the passenger rule, enforced). It
refuses to run when the pane holds nothing for you, verifies the standing notes survived, and
verifies the marker count before it writes. `send` appends below whatever is already pending,
so an unconsumed message is never overwritten (fold-forward, enforced).

You do not need the script — the protocol is the point, and a careful chat can follow it by
hand. The script exists because "careful" is exactly what a chat under time pressure stops
being.

## What this protocol is for

It is a mailbox, not a chat. It works because every message is short, states what happened
and what is needed, and points at the document where the full record lives. If a message is
getting long, the record it should point at has not been written yet — write that first.

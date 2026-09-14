# claude-relay

**A mailbox and an operating model for running one project across several Claude chats.**

Plain Markdown. No server, no plugin, no API. Works in any folder every chat can read — an
[Obsidian](https://obsidian.md) vault is the nicest home, but nothing depends on it.

---

## The problem

Once a project is big enough, one chat is the wrong shape for it. You want one chat that
keeps the record, one that runs the build, one that gives legal and security judgement —
each with its own context, its own files, its own way of thinking. But chats cannot talk to
each other, so *you* become the courier: copying a message out of one window and pasting it
into another, forty times a day, and quietly losing the ones you forgot.

This repo is the fix that fell out of doing exactly that for a few months on a real product
build — a solo founder, three specialised chats, a coding agent, and a launch to hit. Two
things came out of it that turned out to be worth sharing:

1. **The open-pane relay** — a file-based mailbox where each chat has one outbox, messages
   are visible at the top in plain text, and *reading is clearing*. It has a short list of
   rules, each of which exists because its absence lost a message.
2. **The operating model** — the roles, ownership and discipline that make several chats
   behave like a team instead of a crowd: one writer per file, a handoff contract, gate by
   risk, documentation by enumeration, and a rule that the human's asks are never buried.

Both ship here as **Claude skills**: a `SKILL.md` that teaches the chat the protocol, plus a
small script that does the mechanical parts and refuses the dangerous ones.

---

## What a pane looks like

```markdown
# FROM BUILD - outbox

Everything between the rules below is an UNREAD message, in plain view on purpose. ...

---

**ROUTING SHIPPED — three commits (build -> review, ACTION: review) — 2026-01-14**

- ten links across eight surfaces now route by session; /build itself untouched
- the empty-board CTA docks instead of navigating away
- Ask: row sync only.

---

%%
**RECEIPT rev-2026-01-14-a** — consumed the routing ship; recorded on the board; nothing owed.

PROTOCOL — THE OPEN PANE. ...
STANDING NOTES (build's — preserved verbatim by everyone)
...
%%
```

The visible part is the mail. The part between the `%%` markers is the meta — receipts, the
protocol header, the owner's standing notes — which Obsidian hides in reading view and every
other editor simply shows at the foot of the file. Either way the human can open the folder
and *see* what is pending without asking anyone. That visibility is the whole design: **a
pending message the human can see makes them a check on the process; a hidden one makes them
someone the chats can quietly fail in front of.**

## The rules, in one breath

Read every pane first thing, every turn. One action recipient per message. Reading is
clearing — consume, delete, write a receipt, one motion. Never overwrite your own unconsumed
message; fold it forward, and never drop an ask in a fold. Before you clear anything, look
for riders addressed to somebody else and carry them forward — clearing is destructive, so
read what you are destroying. Durable facts go to the record before they ride the relay.
The human is input, never transport.

The full text, with the reasons, is in [`skills/chat-relay/SKILL.md`](skills/chat-relay/SKILL.md).

## Let your Claude adopt it for you

The fastest path is [`ADOPT.md`](ADOPT.md): one prompt you paste into a Claude that can see
this repo. It reads the skills, explains them back, asks you four setup questions, installs
the skills the way your session allows, creates the panes, writes your project instructions,
and dry-runs one message. Using ChatGPT or another assistant for some roles?
[`USING-WITH-OTHER-AIS.md`](USING-WITH-OTHER-AIS.md).

## Quick start

```bash
# 1. create the panes in your project (any folder all the chats can reach)
python3 skills/chat-relay/scripts/relay.py init  docs/RELAY --roles review build compliance

# 2. see what is pending
python3 skills/chat-relay/scripts/relay.py status docs/RELAY

# 3. send
python3 skills/chat-relay/scripts/relay.py send docs/RELAY --from build --to review \
    --title "ROUTING SHIPPED" --body-file msg.md

# 4. consume (removes ONLY what is addressed to you; writes your receipt; keeps everyone else's mail)
python3 skills/chat-relay/scripts/relay.py consume docs/RELAY --pane build --as review \
    --receipt "consumed the routing ship; recorded on the board; nothing owed."
```

The script guards every destructive step: it refuses to clear a pane that holds nothing for
you, refuses to write the comment marker into a visible body, verifies the standing notes
survived, and lands every write by atomic replace. You do not need it — a careful chat can
follow the protocol by hand — but "careful" is exactly what a chat under time pressure stops
being.

## Installing the skills

**Claude Code** — copy the two folders under `skills/` into `.claude/skills/` in your project
(or `~/.claude/skills/` for every project). Claude loads a skill when the task matches its
description, or when you name it: `/chat-relay`.

**Claude.ai / desktop app** — zip each skill folder (`chat-relay/`, `multi-chat-operating-model/`)
and upload it under *Settings → Capabilities → Skills*.

**Anything else** — the `SKILL.md` files are plain Markdown. Paste them into a system prompt
or a project's instructions and the protocol works just the same.

## Setting up a project

1. Copy [`skills/multi-chat-operating-model/templates/PROJECT-INSTRUCTIONS.md`](skills/multi-chat-operating-model/templates/PROJECT-INSTRUCTIONS.md)
   into your project's instructions, fill in the roles and who owns which files, and delete
   what does not apply.
2. Run `relay.py init` to create the panes.
3. Open one chat per role, give each the same instructions, and tell it which hat it wears.
   From then on its first motion every turn is the relay pass.

[`examples/three-role-setup.md`](examples/three-role-setup.md) walks through a day in the life
of a review / build / compliance trio.

## The rules that were hardest to learn

A few of the operating-model rules are worth stating here because they are the ones people
push back on until they have lost an evening to them.

- **Single writer per file.** Every document has exactly one chat that writes it. A change
  you need in someone else's file is a one-line note to its owner, not an edit.
- **State prohibitions as actions, not roles.** *"Write nothing under `docs/system/`"* is
  checkable by the agent about to write. *"The build chat owns that"* asks the agent to first
  know who it is — the very fact in dispute when boundaries get crossed.
- **A gate is worth exactly what its negative case can see.** A check that has never failed
  has not been proven to exist. Make every guard fail once on purpose before trusting it.
- **A document sitting adjacent to a fact is not the fact.** A changelog entry is not the
  edit; a report that says a doc was updated is a claim to verify on disk, never a receipt.
- **Only the human mints identifiers.** A chat that numbers its own findings turns the
  backlog into a holding pen that grows faster than the work.
- **The ask is the last thing trimmed.** Every reply that needs the human ends with a short
  numbered *Needs you* list. Length discipline cuts the retelling, never the record, and
  never an ask.

## Layout

```
ADOPT.md                  a prompt that lets your Claude adopt this for you
USING-WITH-OTHER-AIS.md   ChatGPT, Gemini, mixed setups
skills/
  chat-relay/
    SKILL.md              the protocol, with reasons
    scripts/relay.py      init · status · send · consume
    templates/pane.md     what a fresh pane looks like
  multi-chat-operating-model/
    SKILL.md              roles, ownership, gates, docs, findings, "Needs you"
    templates/PROJECT-INSTRUCTIONS.md
examples/
  three-role-setup.md
```

## License

CC0 1.0 Universal (public domain dedication). Take it, change the role names, keep the rules that earn their place and drop the ones
that don't — and if you find a new way to lose a message, open an issue; that is how every
rule here was written.

---
name: multi-chat-operating-model
description: The operating model for running one project across several specialised Claude chats — named roles with one writer per file, a handoff contract, gate-by-risk, documentation by enumeration, batched writes, and the "Needs you" rule that keeps the human's asks from being buried. Use it when setting up a multi-chat project, writing or revising a project's instructions file, deciding which chat owns a document, or whenever a chat is about to produce another chat's artifact.
---

# Running a project across several chats

One person, one project, several Claude chats — each wearing a named hat, each owning
different files, all coordinating through the [chat-relay](../chat-relay/SKILL.md). This
skill is the set of rules that make that arrangement stable instead of chaotic. They were
learned the hard way on a real solo-founder product build; every one of them exists because
its absence cost an evening.

Read this when you are setting a project up, when you are writing the project's instructions
file, and whenever you notice yourself about to do another role's job.

## 1. Name the hat you are wearing

Every chat has a **role** with a one-line remit and a list of files it owns. A typical
three-role split:

| Role | Remit | Owns |
|---|---|---|
| **Review / tracker** | keeps the record — the tracker, the archive, the dashboard; hands the builder *briefs* | the tracker files, the process reference, its own relay pane |
| **Build / PM** | turns decisions and briefs into executable prompts for a coding agent, runs the build, reports back | every technical and product document not owned by review, its own relay pane |
| **Compliance / security** | legal, privacy, security and compliance judgement | its own relay pane only |

The human owns strategy, design, decisions, the terminal, and commits.

**Single writer per file.** Every document has exactly one chat that writes it. A change
needed in a file you do not own is not yours to make: **name the file and the change in one
line for its owner**, and move on. The relay panes are the one exception (a recipient edits
another chat's pane only to consume a message addressed to it).

**The handoff contract.** Review produces briefs. Build produces prompts. Compliance produces
judgement. **No chat produces another chat's artifact.** A brief that contains a prompt, or a
prompt that contains a legal ruling, is a role boundary being crossed — and the crossing is
where mistakes hide, because nobody is checking that seam.

## 2. State prohibitions as actions, not roles

An instruction must be **checkable from the seat of whoever must obey it**. *"Write nothing
under `docs/system/`"* can be verified by the agent against the path it is about to write.
*"The build chat writes that file"* requires the agent to first know who it is — which is
exactly the fact in dispute when a boundary gets crossed. **An instruction that depends on
the reader correctly identifying themselves is not a constraint, it is a hope.** Name the
forbidden action and the observable, never the actor.

## 3. Gate by risk

The default is **build and report**: the builder ships, names the behavioural check that
proves it works, and reports. A *design handback before code* — the plan shown and ruled on
before anything is built — is reserved for four classes of change: **the core engine, data
migrations, security, and money.** Everything else moves at the speed of a report.

"Let it rip" from the human means fewer gates. It never folds away a migration's stop
(*generate, show the SQL, wait*), a backup before a destructive change, or a secret's custody
rule. A gate deviation is the human's ruling alone and is recorded **with its basis** on the
owning row, so it reads as ruled, never as skipped.

**A gate is worth exactly what its negative case can see.** A check that has never been seen
to fail has not been proven to exist. Before trusting any guard — a test, a lint, a build
step — make it fail once on purpose.

## 4. Documents are maintained by enumeration, not intent

"Update the docs" is not an instruction. Every brief **names its documentation impact by
filename** or states *Docs: none* with the reason. Work is not done until the named documents
are version-bumped on disk. A report that says a document was updated is a **claim to verify
on disk, never a receipt** — the artefact can be present, current and correctly versioned and
still not say the thing you are relying on it to say.

Version markers are **enumerated per file, never recalled from memory**: some files carry a
marker in front-matter, some in a header line, some in a footer, and the one that spells its
marker differently is the one that drifts.

**A document sitting adjacent to a fact is not the fact.** A changelog entry is not the edit.
A provenance record is not an authorship record. A comment citing an authority is not the
authority. When a document is offered as settling something, name the fact you need and ask
whether the document *asserts* it or merely sits next to it.

## 5. Batch writes; keep the record uncapped and the retelling short

Tracker, dashboard and reference documents are written at **milestone close, decision
checkpoint, session end, or on request** — not after every message. Write immediately only
for a live defect, a security or cost exposure, a decision that would otherwise be lost, or a
glance surface a reader would be misled by (a stale status, a closed decision shown open, an
ask already answered still listed).

Length discipline is token discipline, and the ceiling is on the **retelling**, never the
**record**. A handoff is decisions, not derivations: one to three lines per item, about
twenty-five lines per handoff. One finding is one sentence; its general form, if any, gets one
more. Banked rules are cited by name — *"same shape as the passenger rule"* is a complete
reference. Praise is one clause. Receipts are ten lines at most. The full reasoning lives in
**one** place; everything else points at it.

## 6. Findings have three dispositions, and a tracked item is the rarest

When something is found mid-work, it is one of:

1. **A momentary diversion** — go look, fix it, get back to the real work. Nothing written down.
2. **A note on an existing row, with its own trigger** — it must survive the session but
   belongs to something already on the board.
3. **A tracked item with its own identifier** — only when it is genuinely being *deferred*
   and needs its own trigger, severity and close event.

**Only the human mints identifiers.** A chat that numbers its own findings turns the backlog
into a holding pen that grows faster than the work. A correction already in flight is not
debt. A question you are actively answering is not debt. And a handback header is not an
identifier — match the *work* to a row, never the label.

## 7. "Needs you" — the ask is the last thing trimmed

Any reply, brief, relay message or report that needs the human to do, decide, provide,
confirm or look at anything ends with a short numbered list under **Needs you** — one line
per ask, what it is and what it unblocks; decisions state the options. If nothing is needed,
say *Needs you: nothing*.

Two corollaries. **A dated ask is not restated before its date** — repeating it is noise, and
a Needs-you list only holds authority while every line on it is actionable today. And **the
human is input, never transport** — they are never asked to relay, poke, or clear a message
on a chat's behalf.

## 8. Settled topics stay settled

Keep a short list in the project instructions of things ruled and closed — the deploy path,
the backup posture, the decision not to add a linter yet — and never re-raise them. A routine
motion the human makes constantly is never an open item or a reported tail.

## Setting up

1. Copy `templates/PROJECT-INSTRUCTIONS.md` into your project's instructions (or CLAUDE.md /
   system prompt), fill in the roles and file ownership, and delete what does not apply.
2. Run `chat-relay`'s `relay.py init` to create the panes.
3. Give each chat the same instructions file and tell it which hat it wears in its first
   message. The relay pass is its first motion from then on.

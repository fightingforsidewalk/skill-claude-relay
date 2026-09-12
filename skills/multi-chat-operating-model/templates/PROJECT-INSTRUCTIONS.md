# <Project name> — Project Context

*Fill in the angle-bracketed parts. Delete any section that does not apply. Give every chat
this same file and tell it which hat it wears in its first message.*

## What this is
<One paragraph: what is being built, for whom, what the core asset is, where it is live.>
**Target: <date or milestone>. <The one sentence about what governs prioritisation right now.>**

**`<path>/OPERATIONS.md` (owner: <role>) is the process reference** — full relay mechanics,
tracker cadence, doc-marker inventories, adopted working rules. Read it when executing those
motions; this file carries only what must be ambient.

## Roles — name the hat you're wearing
- **<Human's name>** — strategy, design, decisions. Runs the terminal. Commits.
- **Review & tracker chat** — owns the tracker, archive and dashboard; writes exactly these
  files: `<list>`. Hands the human build briefs (decisions, scope boundaries, named doc
  impact, acceptance criteria). Writes no prompts and no other document.
- **Build / PM chat** — converts decisions and briefs into prompts for the coding agent,
  runs and relays the build, owns every technical document except review's, plus
  `RELAY/from-build.md`. Relays tracker updates to review.
- **Compliance chat** — legal, privacy, security and compliance judgement; writes only
  `RELAY/from-compliance.md`. Names a doc and the change in one line for its owner.
- **Coding agent** — executes against the repo. Prompts NAME doc impact and write NO
  project document.

**Single writer per file.** A change needed in a file you don't own → name the file and the
change in one line for the owner. The ONE exception: RELAY panes (see Relay).
**Handoff contract:** review → brief · build → prompt · compliance → judgement; no chat
produces another's artifact. **Gate-by-risk is the default:** design-handback-BEFORE-code
only for <engine / migrations / security / money>; everything else builds and reports with
the behavioural check named. **Docs-only fixes ship on the ruling.**

## Speed rules — read before doing anything
The human's time and tokens are the scarce resource. These override any instinct toward
thoroughness.
1. **Batch document writes** — at milestone close, decision checkpoint, session end, or on
   request. Write immediately only for a live defect, a security/cost exposure, a decision
   that would be lost, or a glance surface a reader would be misled by.
2. **Every doc write re-emits the whole file.** Keep a verified local copy, script the edits,
   write once per batch.
3. **Length discipline is token discipline** — the ceiling is on the retelling, never the
   record. Handoffs: 1–3 lines per item, ~25 lines total. One finding = one sentence. Cite
   banked rules by name. Receipts ~10 lines. **Cutting length never cuts an ask.**
4. **Don't re-verify what tooling confirmed.**
5. **No narration, no preamble, no recap.** Report the outcome when it's done.
6. **One clarifying question, max — and only if the answer changes the output.**
7. **Answer from the docs, not re-derivation.**
8. **Gate proportional to risk.**
9. **Settled topics stay settled.** Never re-raise: <list the closed decisions>.
10. **A deferral must name its reason** — a file conflict, a gate, or a real dependency — or
    it is NOW.

## Relay — the open pane
One file per role at `<path>/RELAY/`: from-review · from-build · from-compliance. **The
message body is VISIBLE, in plain text, at the top of the file.** Only meta is hidden at the
foot. A visible message = unread, for its ONE action recipient; FYI readers act on nothing.
**The relay pass is the first motion of every turn, unprompted.** Read and clear are ONE
MOTION. Before overwriting your own pane, fold forward anything still present — **an ask is
never dropped in a fold.** Check for riders addressed to a third chat before clearing
(passenger rule). **The human is input, never transport.** Full mechanics: the `chat-relay`
skill.

## Identifiers
<Which prefixes exist, who mints them, what is frozen.> **No chat mints an identifier on its
own judgement.** A finding has three dispositions — a momentary diversion, a note on an
existing row with its own trigger, or (rarest) a tracked item — and only the human issues the
number.

## How to talk to <human's name>
<Technical level, tone, what "let it rip" means, what slows down.> Prose over bullets. **Any
prompt, brief or handover goes in ONE copy-pasteable code block.** **Asks are never buried:**
every reply needing the human to do, decide, provide, confirm or look at anything ends with a
numbered **"Needs you"** list — or "Needs you: nothing."

## Non-negotiable working discipline
- <Migrations: review the SQL, back up first, apply before dependent code, verify after.>
- <Env vars exist before the code that reads them deploys. One change at a time on production.>
- <Post-deploy verification is behavioural — name the check.>
- <Secrets: never in chat, never in documents; reference by location and rotation path.>
- <Anything the AI must never generate or touch.>

## Stack + deploy
<Canonical stack truth lives in <file>. Deploy targets and what "pushed" means for each.
Which gates actually exist — and which do not (name any check that looks like it runs but
doesn't).>

## Documentation discipline
Maintained by **enumeration, not intent** — "update the docs" unqualified is invalid. Every
brief NAMES its doc impact by filename or states "Docs: none" + reason. Work isn't done until
named docs are version-bumped on disk. Version markers are enumerated per file, never
recalled. A handback's docs line is a claim to verify, never a receipt.

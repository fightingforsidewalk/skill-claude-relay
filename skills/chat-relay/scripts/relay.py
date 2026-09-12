#!/usr/bin/env python3
"""relay.py — the open-pane relay, mechanised.

    relay.py init    RELAY --roles review build compliance
    relay.py status  RELAY
    relay.py send    RELAY --from build --to review --title "TITLE" --body-file msg.md [--date YYYY-MM-DD]
    relay.py consume RELAY --pane build --as review --receipt "text" [--receipt-file f]

Every write is temp-file + atomic replace. Every destructive step is guarded:
  * consume removes ONLY messages whose ACTION recipient is --as; others stay (passenger rule)
  * consume refuses when the pane holds nothing for you
  * send appends below pending messages; it never overwrites them (fold-forward)
  * standing notes must survive every write, verbatim
  * the marker count must be exactly two after every write, and the visible/hidden
    sides are checked separately — check the side, not the count.

The comment marker is built as chr(37)*2 so it never appears literally in this file.
"""
import argparse, datetime, io, os, re, sys

D = chr(37) * 2              # the comment marker — never written literally
RULE = "\n---\n"
EMPTY = "*(no message pending)*"
HEAD_RE = re.compile(r"^\*\*(.+?)\((\w[\w-]*) -> (\w[\w-]*), ACTION: (\w[\w-]*)\)(.*?)\*\*\s*$", re.M)


def read(p):
    return io.open(p, encoding="utf-8").read()


def write_atomic(p, s):
    tmp = p + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(s)
    os.replace(tmp, p)


ROLE_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def check_role(role):
    """Role names become file names. Only [A-Za-z0-9_-] is allowed, so a role can never be a path."""
    if not ROLE_RE.match(role or ""):
        sys.exit("invalid role name %r — use letters, digits, '-' or '_' only" % role)
    return role


def pane_path(d, role):
    check_role(role)
    base = os.path.realpath(d)
    p = os.path.realpath(os.path.join(base, "from-%s.md" % role))
    if os.path.commonpath([base, p]) != base:
        sys.exit("refusing: pane path %r resolves outside the relay directory" % p)
    return p


def split(s):
    """Return (visible, hidden). hidden starts with the first marker line."""
    i = s.find("\n" + D + "\n")
    if i == -1:
        sys.exit("no hidden block found — is this a relay pane?")
    return s[:i], s[i:]


def check_markers(s):
    n = s.count(D)
    if n != 2:
        sys.exit("marker count is %d, expected 2 — refusing to write" % n)


def messages(visible):
    """Parse the visible pane into a list of (heading_match, block_text) tuples."""
    heads = list(HEAD_RE.finditer(visible))
    out = []
    for k, m in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else visible.rfind(RULE)
        out.append((m, visible[m.start():end]))
    return out


def standing_notes(hidden):
    j = hidden.find("STANDING NOTES")
    return hidden[j:] if j != -1 else ""


# ---------------------------------------------------------------- init

PANE_TEMPLATE = """# FROM {ROLE} - outbox

**Everything between the rules below is an UNREAD message, in plain view on purpose.** A message
stays here until its ACTION recipient consumes it; the recipient deletes the message from this pane
and writes its receipt into the hidden block at the foot of the file, in the same motion. If this
pane holds no message, {role} has nothing outstanding. Meta is hidden at the foot deliberately:
the protocol header, the receipt log, and {role}'s standing notes.

---

{empty}

---

{D}
PROTOCOL — THE OPEN PANE. Message bodies are VISIBLE, at the top of this file, in plain text.
This hidden block is META ONLY: this header, the receipt log, and the owner's standing notes.
A visible message = unread, for its ONE action recipient. The recipient DELETES it from the
visible pane and writes its receipt here, in the same turn — read and clear are ONE MOTION.
FYI readers clear nothing. Before overwriting your own visible pane, look at it: a
still-present message is unconsumed and folds forward IN FULL. Durable facts go to the record
BEFORE riding the relay. The human is input, never transport.

OUTBOX OF: {role}

RECEIPT LOG (newest first)

STANDING NOTES ({role}'s — every other chat preserves these verbatim)
(none yet)
{D}
"""


def cmd_init(a):
    os.makedirs(a.dir, exist_ok=True)
    for role in a.roles:
        p = pane_path(a.dir, role)
        if os.path.exists(p) and not a.force:
            print("exists, skipped:", p)
            continue
        write_atomic(p, PANE_TEMPLATE.format(ROLE=role.upper(), role=role, empty=EMPTY, D=D))
        print("created:", p)


# ---------------------------------------------------------------- status

def cmd_status(a):
    any_pending = False
    for f in sorted(os.listdir(a.dir)):
        if not (f.startswith("from-") and f.endswith(".md")):
            continue
        vis, _ = split(read(os.path.join(a.dir, f)))
        msgs = messages(vis)
        if not msgs:
            print("%-22s (nothing pending)" % f)
            continue
        any_pending = True
        print("%-22s %d pending" % (f, len(msgs)))
        for m, _ in msgs:
            print("    -> ACTION: %-12s %s" % (m.group(4), m.group(1).strip()))
    sys.exit(0 if not any_pending else 3)


# ---------------------------------------------------------------- send

def cmd_send(a):
    p = pane_path(a.dir, a.sender)
    s = read(p)
    vis, hid = split(s)
    body = read(a.body_file).strip() if a.body_file else sys.stdin.read().strip()
    if D in body:
        sys.exit("the body contains the comment marker — it would open a hidden block. Refusing.")
    date = a.date or datetime.date.today().isoformat()
    heading = "**%s (%s -> %s, ACTION: %s) — %s**" % (a.title, a.sender, a.to, a.to, date)
    msg = "\n" + heading + "\n\n" + body + "\n"
    last_rule = vis.rfind(RULE)
    if last_rule == -1:
        sys.exit("pane has no closing rule — refusing")
    head = vis[:last_rule]
    if EMPTY in head:
        head = head.replace(EMPTY + "\n", "").replace(EMPTY, "")
        head = head.rstrip() + "\n"
    else:
        # fold-forward: something is pending; append below it, never replace it
        pending = messages(vis)
        print("note: %d unconsumed message(s) already pending — appending below them" % len(pending))
        head = head.rstrip() + "\n"
    new_vis = re.sub(r"\n{3,}", "\n\n", head + msg + RULE)
    out = new_vis + hid
    check_markers(out)
    assert standing_notes(hid) == standing_notes(split(out)[1]), "standing notes changed"
    write_atomic(p, out)
    print("sent to %s via %s" % (a.to, p))


# ---------------------------------------------------------------- consume

def cmd_consume(a):
    p = pane_path(a.dir, a.pane)
    s = read(p)
    vis, hid = split(s)
    msgs = messages(vis)
    mine = [(m, b) for m, b in msgs if m.group(4) == a.me]
    others = [(m, b) for m, b in msgs if m.group(4) != a.me]
    if not mine:
        sys.exit("nothing in from-%s.md is addressed to %s — refusing to clear" % (a.pane, a.me))
    for m, b in mine:
        if re.search(r"ACTION:\s*(\w[\w-]*)", b[len(m.group(0)):]):
            print("WARNING: a message for you mentions another ACTION recipient in its body — "
                  "carry that rider forward in your own pane (passenger rule).")
    new_vis = vis
    for m, b in mine:
        new_vis = new_vis.replace(b, "", 1)
    if not others:
        # pane is now empty: normalise to the empty marker
        first_rule = new_vis.find(RULE)
        new_vis = new_vis[:first_rule] + RULE + "\n" + EMPTY + "\n" + RULE
    else:
        new_vis = re.sub(r"\n{3,}", "\n\n", new_vis)
    receipt = a.receipt or (read(a.receipt_file).strip() if a.receipt_file else None)
    if not receipt:
        sys.exit("a receipt is required — say what you consumed and where you recorded it")
    if D in receipt:
        sys.exit("the receipt contains the comment marker — refusing")
    stamp = a.date or datetime.date.today().isoformat()
    rid = "**RECEIPT %s-%s-%s** — " % (a.me[:3], stamp, a.suffix)
    j = hid.find("RECEIPT LOG (newest first)")
    if j == -1:
        # older panes: put the receipt right after the opening marker
        new_hid = hid[: len("\n" + D + "\n")] + rid + receipt + "\n\n" + hid[len("\n" + D + "\n"):]
    else:
        k = j + len("RECEIPT LOG (newest first)\n")
        new_hid = hid[:k] + "\n" + rid + receipt + "\n" + hid[k:]
    out = new_vis + new_hid
    check_markers(out)
    assert standing_notes(hid) == standing_notes(split(out)[1]), "standing notes changed — refusing"
    left = messages(split(out)[0])
    assert all(m.group(4) != a.me for m, _ in left), "a message for you survived the clear"
    assert len(left) == len(others), "a message for someone else was lost — refusing"
    write_atomic(p, out)
    print("consumed %d message(s) for %s; %d left for others; receipt written" % (len(mine), a.me, len(others)))


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("dir"); s.add_argument("--roles", nargs="+", required=True)
    s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("status"); s.add_argument("dir"); s.set_defaults(fn=cmd_status)

    s = sub.add_parser("send"); s.add_argument("dir")
    s.add_argument("--from", dest="sender", required=True); s.add_argument("--to", required=True)
    s.add_argument("--title", required=True); s.add_argument("--body-file"); s.add_argument("--date")
    s.set_defaults(fn=cmd_send)

    s = sub.add_parser("consume"); s.add_argument("dir")
    s.add_argument("--pane", required=True, help="role whose pane holds the message (e.g. build)")
    s.add_argument("--as", dest="me", required=True, help="your role")
    s.add_argument("--receipt"); s.add_argument("--receipt-file"); s.add_argument("--date")
    s.add_argument("--suffix", default="a", help="letter to disambiguate several receipts in one day")
    s.set_defaults(fn=cmd_consume)

    a = ap.parse_args()
    for attr in ("sender", "to", "pane", "me"):
        if getattr(a, attr, None) is not None:
            check_role(getattr(a, attr))
    for r in getattr(a, "roles", None) or []:
        check_role(r)
    a.fn(a)


if __name__ == "__main__":
    main()

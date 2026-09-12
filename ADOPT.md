# Adopting this with your own Claude

The fastest way to adopt this repo is to let your Claude read it first and then walk you
through the setup. Paste the prompt below into a Claude that can see these files — Claude
Code opened in the cloned repo, the desktop app with the folder connected, or a claude.ai
project with the files uploaded. If your Claude can only see pasted text, paste the two
`SKILL.md` files and this prompt together.

## The prompt

```
You are helping me adopt the "claude-relay" repo: a file-based mailbox protocol and an
operating model for running one project across several specialised Claude chats. Read
README.md, skills/chat-relay/SKILL.md, skills/multi-chat-operating-model/SKILL.md,
skills/chat-relay/scripts/relay.py and examples/three-role-setup.md before you say anything.

Then do the following, in order, pausing for my answer wherever you ask a question:

1. EXPLAIN IT BACK. In plain language, under 200 words: what problem the relay solves, what a
   pane file is, and the five rules you consider most important. If anything in the repo is
   unclear or contradictory, say so now rather than later.

2. CHECK WHAT YOU CAN DO FROM HERE. Tell me honestly whether, in this session, you can
   (a) read and write files in a folder on my machine, (b) run Python, (c) install a skill.
   The adoption path depends on this; do not guess.

3. ASK ME THE SETUP QUESTIONS — one at a time, and only these:
   - What is the project, in one line?
   - Which roles do I want? (Suggest review / build / compliance, and explain what each owns,
     but let me rename, add or drop roles.)
   - Where should the shared folder live? (An Obsidian vault is recommended because it hides
     the meta block in reading view; any folder every chat can reach is fine.)
   - Which AI tools will each role run in? (Claude Code, the Claude desktop app, claude.ai
     projects, or something else — see USING-WITH-OTHER-AIS.md.)

4. INSTALL THE SKILLS, in the way that matches step 2:
   - Claude Code: copy skills/chat-relay and skills/multi-chat-operating-model into
     .claude/skills/ in my project (or ~/.claude/skills/ for all projects). Confirm by
     listing them.
   - Claude desktop / claude.ai: tell me to zip each skill folder and upload it under
     Settings -> Capabilities -> Skills, and wait for me to confirm.
   - No skill support: tell me to paste both SKILL.md files into the project's instructions
     (or the system prompt), and give me the exact text to paste.

5. CREATE THE PANES. If you can run Python, run:
     python3 skills/chat-relay/scripts/relay.py init <folder>/RELAY --roles <my roles>
   and show me the result of `relay.py status`. If you cannot, generate each pane file's
   contents from skills/chat-relay/templates/pane.md and tell me exactly where to save them.

6. WRITE MY PROJECT INSTRUCTIONS. Start from
   skills/multi-chat-operating-model/templates/PROJECT-INSTRUCTIONS.md, fill in everything I
   have told you, mark anything you had to leave as a placeholder, and give me the whole file
   in one code block so I can paste it into each chat's project instructions.

7. DRY-RUN THE PROTOCOL. Send one test message from one role to another with relay.py send
   (or by hand), show me the pane, then consume it and show me the receipt. Then tell me, in
   three lines, what the first motion of every turn is from now on and what I must never be
   asked to do (I am input, never transport).

8. END WITH "NEEDS YOU": a numbered list of anything still on me, one line each. If nothing,
   say "Needs you: nothing."

Do not skip steps, do not merge steps, and do not start step 4 before I have answered step 3.
```

## After it runs

Open one chat per role. Give each the same project instructions, and tell it which hat it
wears in your first message. From then on its first motion every turn is the relay pass —
you should never again need to copy a message between windows.

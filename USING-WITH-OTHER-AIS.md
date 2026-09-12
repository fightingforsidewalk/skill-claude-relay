# Using this with ChatGPT, Gemini, or anything else

Nothing here is Claude-specific. A "skill" is a Markdown file of instructions plus a small
Python script; a pane is a Markdown file in a folder. Any assistant that can read
instructions and either touch files or read pasted text can take a role.

## What each tool needs

| The role's assistant needs to… | Claude Code / desktop | claude.ai project | ChatGPT (Custom GPT / Project) | Gemini / other |
|---|---|---|---|---|
| know the protocol | install the skill, or paste SKILL.md into instructions | paste SKILL.md into project instructions | paste SKILL.md into the GPT's / project's instructions | paste SKILL.md into the system prompt |
| read the panes | reads the folder directly | you paste the pane, or upload it | with file access (desktop app / connector): reads directly; otherwise you paste | you paste |
| write its own pane and consume others' | edits the folder directly | gives you the text to save | with file access: directly; otherwise gives you the text | gives you the text |
| run `relay.py` | yes | no — you run it, or skip it | with a code tool that can see your folder: yes; otherwise you run it | you run it |

The protocol survives the "you paste" path — that is how it started — but every rule in it
exists to make the human **not** the courier. The more roles that can read and write the
folder directly, the more the protocol pays for itself. Mixed setups work fine: a Claude
Code builder that edits panes directly, a ChatGPT compliance role you paste to.

## Two things to keep exactly the same across tools

1. **The pane shape.** Visible body at the top, hidden meta between the `%%` markers at the
   foot, one ACTION recipient per message heading. Every assistant must produce and parse
   the same shape, or `status` and `consume` stop being trustworthy.
2. **The rules.** Reading is clearing. Never overwrite an unconsumed message. Never drop an
   ask. Check for riders before clearing. Durable facts go to the record before the relay.
   The human is input, never transport.

## The hidden block outside Obsidian

`%%` is an Obsidian comment marker; other editors simply show the block at the foot of the
file. That is fine — it is meta, not mail — but the delimiter hazard still applies: never
write the marker inside a visible body, and keep syntax balanced inside the block. If you
would rather use HTML comments (`<!-- … -->`), change `D` in `relay.py` and the templates
consistently; the protocol does not care which marker it is, only that there are two.

# Using the rules with Claude Code

This repo is also a Claude Code plugin, **python-rules**, distributed from
its own marketplace, **romkey-python**.

## Install

In Claude Code:

```
/plugin marketplace add romkey/python-ai-rules
/plugin install python-rules@romkey-python
```

Or from a shell:

```bash
claude plugin marketplace add romkey/python-ai-rules
```

```bash
claude plugin install python-rules@romkey-python
```

## Commands

| Command | What it does |
|---------|--------------|
| `/python-rules:new [name]` | Scaffolds a project from `templates/`, asks what it does and whether it needs a database, fills in placeholders, looks up current versions, runs the tests and lint. Doesn't create a GitHub repo or push unless you ask. |
| `/python-rules:check [fix]` | Audits the current repo against RULES.md and reports findings by section. With `fix`, applies them and re-runs the tests and lint. |
| `/python-rules:release [patch\|minor\|major]` | Releases per [releasing.md](releasing.md): checks CI, proposes the bump from the changelog, runs the Release workflow and reports the release PR. |

There is also a **rules** skill that Claude loads by itself when it works on
Python code, Docker or CI in a repo that follows these rules, so you don't
have to paste RULES.md into the conversation.

## Updating

```bash
claude plugin marketplace update romkey-python
```

```bash
claude plugin update python-rules@romkey-python
```

Then restart Claude Code or run `/reload-plugins`. The plugin's version
follows this repo's release tags.

## Without the plugin

Every project's `AGENTS.md` (symlinked as `CLAUDE.md`) says to follow
RULES.md, which works with Claude Code and other AI tools. Or just tell the
assistant: "Follow https://github.com/romkey/python-ai-rules/blob/main/RULES.md".

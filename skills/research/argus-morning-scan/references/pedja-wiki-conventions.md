# Vault / Wiki Conventions — TEMPLATE

How Argus writes notes into your Obsidian vault. Customize folder names to match
your own vault structure. The skill references this file by the name
`pedja-wiki-conventions.md` — keep the filename, edit the contents.

## Vault Layout (relative to OBSIDIAN_VAULT_PATH)
```
wiki/
├── synthesis/     # Argus's daily scans + weekly roll-ups (the main output)
├── inbox/         # content handoff JSON for a downstream writer
├── entities/      # optional: people, companies, products pages
└── log.md         # append-only one-line index of what was written each run
raw/               # immutable: never written to by Argus
```

## Note-Writing Rules
- **Daily scan** → `wiki/synthesis/argus-scan-{YYYY-MM-DD}.md` using the synthesis
  template (`templates/synthesis-scan.md`). YAML frontmatter with `type`, `date`, `tags`.
- **Weekly roll-up** → `wiki/synthesis/argus-week-{YYYY-WNN}.md`.
- **Content handoff** → `wiki/inbox/argus-handoff-{YYYY-MM-DD}.json` per `handoff_schema.json`.
- **After every write**, append one line to `wiki/log.md` (date, file written, signal count).
- Use `[[wikilinks]]` to cross-reference related entity/concept pages when they exist.
- **Never modify anything in `raw/`.** That layer is immutable input, not output.

## Frontmatter Standard
Every synthesis note starts with:
```yaml
---
type: argus-scan        # or argus-week
date: YYYY-MM-DD
tags: [scan, <your-domain-tag>]
---
```
Consistent frontmatter is what makes Dataview / search across your vault work.

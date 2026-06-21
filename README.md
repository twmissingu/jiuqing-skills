[![English](https://img.shields.io/badge/English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/中文-red.svg)](README_zh.md)

---

# Skills

A cross-platform skill library for AI agents — write each capability once, use it everywhere.

## Why This Project?

AI coding agents (Codex, Claude Code, OpenCode, and more) each scan their own flat `skills/` directory. Maintaining the same capability separately for every platform is tedious and drifts out of sync.

This repo is the **single source of truth**. Every skill is a self-contained `SKILL.md`; each platform symlinks back here, so you maintain in one place and it takes effect everywhere. Skills declare dependencies on one another via a `depends` field, and the agent loads the dependency chain on demand.

## Features

- 🧩 **Composable** — skills reference each other through `depends`; base skills are reused, not duplicated
- 🔗 **Single source of truth** — one repo, symlinked into every platform's skill directory
- 🗂️ **Three domains** — `core` (foundational), `dev` (engineering), `content` (creation)
- ✅ **Align before acting** — `jiuqing-idea-grill` interrogates the plan before any irreversible step
- 🔒 **Secret-safe** — generation scripts read keys only from environment variables, never hardcoded

## Skill Catalog

Skills are named `jiuqing-<noun>-<verb>`: the fixed prefix `jiuqing` + a noun + a verb, hyphen-joined, all lowercase, no abbreviations. The directory name matches the `name` field in the frontmatter.

### core — foundational capabilities

| Skill | Purpose |
|-------|---------|
| `jiuqing-idea-grill` | Interrogate a plan/requirement/intent one item at a time and align before acting — callable directly, or referenced by other skills via `depends` as a pre-execution alignment step |
| `jiuqing-roles-debate` | Review and stress-test a deliverable (doc, project, code, design) from multiple roles/perspectives across rounds until a consensus conclusion |
| `jiuqing-session-handoff` | Compress the current session into a handoff doc for switching models or agent platforms, or for starting a fresh session |
| `jiuqing-skill-create` | Scaffold a new skill in the standard format |
| `jiuqing-skill-evolve` | Iteratively improve and evolve an existing skill against scored feedback |

### dev — engineering capabilities

| Skill | Purpose |
|-------|---------|
| `jiuqing-agents-inject` | Inject/initialize agent behavior rules into a project's AGENTS.md |
| `jiuqing-bug-diagnose` | Systematically locate and diagnose stubborn bugs and performance regressions |
| `jiuqing-context-sync` | Extract domain concepts into a glossary / CONTEXT.md to unify project terminology |
| `jiuqing-goal-set` | Set a release-focused project goal and produce a goal prompt for an agent |
| `jiuqing-prd-write` | Turn a discussion into a PRD / product requirements doc |
| `jiuqing-product-polish` | Autonomously iterate and polish a project toward a shippable state |
| `jiuqing-project-ship` | Gate the whole pre-release pipeline (security, legal, quality, version, docs) |

### content — creation capabilities

| Skill | Purpose |
|-------|---------|
| `jiuqing-image-generate` | Generate images from a text prompt |
| `jiuqing-video-generate` | Generate a video clip from a text prompt |
| `jiuqing-prompt-refine` | Refine a short idea into a professional image/video generation prompt |

## Directory Structure

```
skills/
├── core/       # Foundational domain — shared capabilities others compose on
├── dev/        # Engineering domain — requirements, review, release checks, etc.
├── content/    # Content domain — prompt refinement, image/video generation, etc.
├── scripts/    # Tooling (e.g. sync.sh for multi-platform symlinks)
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## SKILL.md Standard

Every skill must follow this frontmatter format:

```yaml
---
name: jiuqing-<noun>-<verb>
description: One-line description of what the skill does
category: core | dev | content
depends: []    # optional, references the name of other skills
---
```

The body is the behavioral specification the agent executes.

## Composition Rules

- Skills under `core/` are base capabilities; other domains reference them via `depends`
- A composing skill explicitly states in its body which base skills it draws on
- At runtime the agent decides whether to load a base skill based on `depends`

## Align Before Acting

`core/jiuqing-idea-grill` provides the "align information before acting" capability: it interrogates the plan and requirements one item at a time, like an interview, and reaches consensus before any work begins. A skill that needs this step declares `jiuqing-idea-grill` in `depends`; fixed-script skills that do not declare it run directly without triggering alignment.

## Quick Start

### Prerequisites

- `bash` and `git`
- An agent platform with a flat `skills/` directory (Claude Code, Codex, OpenCode)

### Installation

```bash
git clone git@github.com:twmissingu/jiuqing-skills.git
cd jiuqing-skills
./scripts/sync.sh            # symlink each skill into every platform directory
./scripts/sync.sh --dry-run  # preview only, no changes
```

`sync.sh` symlinks into the following existing platform directories (missing ones are skipped automatically):

| Platform | Directory |
|----------|-----------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

On a name clash the script skips and warns — it never overwrites existing content. Re-running is idempotent.

> zcode uses a plugin-marketplace mechanism (not a local flat directory), so it is not symlinked here; it must be packaged as a plugin separately.

### Staying Up to Date

- **Update an existing skill's content**: `git pull` in this repo. Symlinks point to the source, so every platform picks up the latest automatically.
- **Add a new skill**: after `git pull`, re-run `./scripts/sync.sh` to add the new symlinks.

## For AI Agents

1. **Clone and link**
   ```bash
   git clone git@github.com:twmissingu/jiuqing-skills.git
   cd jiuqing-skills
   ./scripts/sync.sh
   ```
2. **Discover** — skills live under `core/`, `dev/`, `content/`; each directory holds one `SKILL.md`. The directory name is the skill name.
3. **Load on demand** — read a skill's frontmatter; if `depends` is set, load the referenced base skills first.

Note: `jiuqing-image-generate` and `jiuqing-video-generate` require the `AGNES_API_KEY` environment variable. The scripts read the key only from the environment — never from files or arguments.

## Contributing

Use `jiuqing-skill-create` to scaffold a new skill in the standard format, then run `./scripts/sync.sh`. Keep one meaning defined in exactly one place, and follow the writing principles in [AGENTS.md](AGENTS.md).

## License

[MIT](LICENSE)

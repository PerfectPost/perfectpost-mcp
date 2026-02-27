# Claude Code Skills — Best Practices

Reference guide for developing, testing, and publishing Claude Code skills. Based on the official skill-creator documentation and lessons learned building this skill.

---

## What is a skill?

A skill is a directory containing a `SKILL.md` file with YAML frontmatter. When installed, its name and description are always present in Claude's context. When the description matches the user's intent, Claude reads the full `SKILL.md` body and follows its instructions.

```
skill-name/
├── SKILL.md          (required)
├── .mcp.json         (optional — auto-configures MCP servers on install)
├── evals/
│   └── evals.json    (test cases — excluded from .skill package)
└── scripts/          (optional — bundled executable scripts)
    references/       (optional — documentation loaded on demand)
    assets/           (optional — templates, fonts, icons)
```

---

## SKILL.md structure

### Frontmatter (YAML)

Only these keys are allowed:

```yaml
---
name: my-skill-name          # kebab-case, max 64 chars, required
description: >               # max 1024 chars, no < or >, required
  What it does and when to trigger it.
license: MIT                 # optional
allowed-tools: [Bash, Read]  # optional — restrict available tools
metadata:                    # optional — arbitrary key/value pairs
  key: value
compatibility: "..."         # optional — describe required dependencies
---
```

### Body

The body is markdown. It loads into context every time the skill triggers. Keep it under ~500 lines. If it grows longer, split content into `references/` files and point to them from the body.

**Three-level loading:**
1. **Frontmatter** (name + description) — always in context, ~100 words
2. **SKILL.md body** — loaded when skill triggers, ideally < 500 lines
3. **Bundled resources** — loaded or executed on demand, unlimited size

---

## Writing the description

The description is the **primary triggering mechanism**. Claude decides whether to use a skill based solely on its name and description.

**Key principles:**
- Include both *what the skill does* and *when to use it*
- Slightly "pushy" descriptions trigger more reliably — Claude tends to undertrigger
- Name specific contexts, use cases, and user phrases that should activate the skill
- Don't put triggering logic in the body — it belongs in the description

**Example of a weak description:**
> "Guide for using the PerfectPost API."

**Example of a strong description:**
> "Guide to configure and use the PerfectPost MCP server to manage LinkedIn content directly from Claude Code. Use this skill whenever the user mentions PerfectPost, wants to read, analyze, or schedule LinkedIn posts, manage drafts, check publication statistics, get engagement data (likes, comments), or automate any LinkedIn content workflow. Trigger even if the user just says 'LinkedIn' and seems to want data or scheduling help."

---

## Bundling an MCP server (.mcp.json)

To auto-configure an MCP server when the skill is installed, add a `.mcp.json` file at the skill root:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://your-mcp-server.example.com/mcp",
      "clientId": "your-oauth-client-id",
      "callbackPort": 6274
    }
  }
}
```

**Important notes:**
- `clientId` and `callbackPort` are needed when the MCP server does not support Dynamic Client Registration (DCR)
- `callbackPort` must match a registered OAuth redirect URI: `http://localhost:<port>/callback`
- Even with `.mcp.json`, users still need to authenticate manually via `/mcp → Authenticate`
- The manual install command equivalent is:
  ```bash
  claude mcp add --transport http --scope user \
    --client-id <client-id> \
    --callback-port <port> \
    <server-name> <url>
  ```

---

## OAuth / MCP authentication

When building a skill that uses a remote MCP server with OAuth:

- Claude Code uses `http://localhost:<port>/callback` as the redirect URI (not `/oauth/callback`)
- The callback port must be declared at MCP registration time (`--callback-port`) and registered in the OAuth provider
- If DCR is not supported, the `client_id` must be pre-registered and shared via `--client-id`
- `--scope user` stores the token per-user in `~/.claude.json` (not per-project)
- Tokens are renewed automatically on next session start after expiry

---

## Writing skill instructions

**Use imperative form:** "Call `list_posts` to get recent posts" not "You might want to call..."

**Explain the why:** Instead of `ALWAYS use HTML for drafts`, explain:
> "Draft content must be HTML — the API stores and renders it as HTML, so plain text will display incorrectly."

**Avoid over-constraining:** Rigid MUSTs and NEVERs make skills brittle. Help Claude understand the reasoning so it can handle edge cases intelligently.

**Define output formats explicitly** when they matter:

```markdown
## Output format
Always present stats as a markdown table with these columns:
| Metric | Value | vs. Previous Period |
```

**Include worked examples** for non-obvious behaviors:

```markdown
## search_posts tip
search_posts does exact string matching. Search for "ChatGPT" not "AI".
Run multiple searches with different keywords for full coverage.
```

---

## Evals (evals/evals.json)

Test cases used by the skill-creator tool to benchmark skill performance.

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user prompt, written as a real user would type it",
      "expected_output": "Description of what Claude should do — which tools to call, in what order, what the output should contain",
      "files": []
    }
  ]
}
```

**Guidelines:**
- Write 2–3 evals covering distinct use cases
- Prompts should be realistic — include personal context, casual language, typos
- `expected_output` describes behavior, not exact wording
- The `evals/` directory is excluded when packaging a `.skill` file
- Assertions (for automated grading) can be added later under an `assertions` key

---

## Packaging

Create a distributable `.skill` file (zip format):

```bash
cd /path/to/skill-creator
python -m scripts.package_skill /path/to/my-skill /output/directory
```

What gets included:
- `SKILL.md`
- `.mcp.json` (if present)
- `scripts/`, `references/`, `assets/` (if present)

What gets excluded:
- `evals/` directory
- `__pycache__/`, `node_modules/`
- `*.pyc`, `.DS_Store`

The `.skill` file can be distributed via a GitHub Release:
```bash
claude skill install https://github.com/org/repo/releases/latest/download/my-skill.skill
```

---

## Description optimization

After the skill is working, use the optimization loop to improve triggering accuracy:

```bash
# From the skill-creator directory
python -m scripts.run_loop \
  --eval-set /path/to/trigger-eval.json \
  --skill-path /path/to/my-skill \
  --model claude-sonnet-4-6 \
  --max-iterations 5 \
  --verbose
```

The eval set is a JSON array of `{ query, should_trigger }` pairs — typically 20 queries, half that should trigger, half that shouldn't (especially near-misses that share keywords but need something else).

---

## Naming conventions

| Item | Convention |
|---|---|
| Skill name | `kebab-case` |
| Script files | `snake_case.py` |
| Workspace directories | `iteration-1/`, `eval-1/`, `run-1/` |
| MCP server names | `lowercase-kebab` |

---

## Common pitfalls

| Problem | Fix |
|---|---|
| Skill never triggers | Strengthen the description with explicit use cases and "trigger even if..." phrasing |
| Skill triggers too broadly | Add negative examples to description or tighten the scope |
| MCP "Dynamic Client Registration not supported" | Add `--client-id` to the mcp add command |
| Wrong OAuth callback URL | Ensure `http://localhost:<port>/callback` is registered (not `/oauth/callback`) |
| SKILL.md fails validation | Check frontmatter keys — only `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility` are allowed |
| `.skill` package includes `.git/` | Output to a separate directory; the packaging script doesn't exclude `.git/` by default |

---

## Checklist before publishing

- [ ] `SKILL.md` frontmatter is valid (run `python -m scripts.quick_validate /path/to/skill`)
- [ ] Description triggers reliably for the intended use cases
- [ ] All instructions are in English (international users)
- [ ] `evals/evals.json` prompts are in English
- [ ] `.mcp.json` is present if the skill requires an MCP server
- [ ] Sensitive values (tokens, secrets) are not hardcoded — only public `client_id` values
- [ ] `.skill` package is attached to the GitHub Release

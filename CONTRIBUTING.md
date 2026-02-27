# Contributing

## Repository structure

```
perfectpost-mcp/
├── SKILL.md                        # Skill definition (frontmatter + instructions)
├── .mcp.json                       # MCP server auto-configuration
├── evals/evals.json                # Test cases (excluded from .skill package)
├── .github/
│   ├── scripts/package.py          # Standalone packaging script
│   └── workflows/release.yml       # CI/CD workflow
└── .actrc                          # Local act configuration
```

## Making changes

Edit `SKILL.md` to update the skill instructions or description. The frontmatter only allows these keys: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`.

## Testing the CI locally

The CI workflow uses `act` to run GitHub Actions locally with Docker.

**Install dependencies:**

```bash
brew install act
# Docker must be running
```

**Run the validate job:**

```bash
cd ~/skills/perfectpost-mcp
act push --job validate
```

The `.actrc` file at the repo root already configures the right Docker image (`catthehacker/ubuntu:act-22.04`). The first run downloads the image (~900 MB).

A successful run ends with:

```
| Packaged: /tmp/dist/perfectpost-mcp.skill
[Release/validate] ✅  Success - Main python .github/scripts/package.py . /tmp/dist
| Skill is valid
[Release/validate] ✅  Success - Main echo "Skill is valid"
[Release/validate] 🏁  Job succeeded
```

## Releasing a new version

```bash
git tag v1.0.0
git push origin v1.0.0
```

The `release` job runs automatically on GitHub and attaches `perfectpost-mcp.skill` to the GitHub Release.

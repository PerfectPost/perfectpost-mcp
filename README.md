# PerfectPost MCP — Claude Code Skill

A Claude Code skill that connects to the [PerfectPost](https://perfectpost.social) MCP server, giving you full control over your LinkedIn content directly from your terminal.

## What you can do

- **Analyze performance**: impressions, likes, comments, engagement rate — for any time period
- **Search your content**: find posts by keyword and compare their engagement
- **Create drafts**: write posts in your own style based on your past publications
- **Schedule posts**: program publications at a specific date and time
- **Manage media**: attach images, videos, or PDFs to a draft from a URL
- **Track engagement**: see who liked or commented on any of your posts

## Installation

### 1. Install the skill

**Option A — via the skills CLI** (requires Node.js):

```bash
npx skills add PerfectPost/perfectpost-mcp
```

**Option B — manual download**:

```bash
curl -L https://github.com/PerfectPost/perfectpost-mcp/releases/latest/download/perfectpost-mcp.skill \
  -o /tmp/perfectpost-mcp.skill
unzip /tmp/perfectpost-mcp.skill -d ~/.claude/skills/
rm /tmp/perfectpost-mcp.skill
```

### 2. Authenticate

In Claude Code, run `/mcp`, select **perfectpost → Authenticate**. Your browser will open for you to log in with your PerfectPost account. Once done, the token is stored automatically.

> **Don't have a PerfectPost account?** Sign up at [perfectpost.social](https://perfectpost.social).

### 3. You're ready

Start a new Claude Code session and try:

```
Show me my LinkedIn stats for last month
```

---

## Manual MCP setup (without the skill)

If you prefer to configure the MCP server directly:

```bash
claude mcp add --transport http --scope user \
  --client-id dnakgf4sbal93ukngisqgb3vo \
  --callback-port 6274 \
  perfectpost https://mcp.perfectpost.social/mcp
```

Then authenticate via `/mcp → perfectpost → Authenticate`.

---

## Example prompts

**Performance analysis**
```
Show me the statistics for my LinkedIn posts from last month.
Which posts performed best in terms of engagement?
```

```
Compare my LinkedIn engagement: last month vs the month before.
Give me impressions, likes, comments in a table.
```

**Content creation**
```
Write a LinkedIn post about the importance of personal branding for developers.
Base it on my last 5 posts to match my style. Create a draft and schedule it for tomorrow at 9am.
```

```
Here's an article I wrote: [paste text].
Turn it into a punchy LinkedIn post, create a draft, and schedule it for Friday at 8:30am.
```

**Content search**
```
Find all my posts that mention AI or machine learning.
Which ones had the most engagement?
```

---

## Available MCP tools

| Tool | Description |
|---|---|
| `list_posts` | List published posts (paginated) |
| `get_post` | Get a full post with all metrics |
| `search_posts` | Full-text search across posts |
| `get_posts_stats_summary` | Aggregated stats for a time period |
| `get_post_likers` | People who liked a post |
| `get_post_commenters` | People who commented on a post |
| `get_linkedin_profile` | Your LinkedIn profile and account stats |
| `list_drafts` | List drafts (filterable by status) |
| `get_draft` | Get a full draft |
| `create_draft` | Create a new draft |
| `update_draft` | Edit an existing draft |
| `schedule_draft` | Schedule a draft for publication |
| `set_draft_media_from_url` | Attach media (image/video/PDF) from URL |
| `update_post` | Update metadata on a published post |

---

## Troubleshooting

**"Unauthorized" or expired token** — Restart Claude Code. The token renews automatically on next use.

**Server not showing in `claude mcp list`** — Re-run the manual MCP setup command above.

**Stats not loading** — Make sure your LinkedIn account is connected to PerfectPost at [perfectpost.social](https://perfectpost.social).

**`search_posts` returns no results** — The tool does exact string matching. Use specific keywords (`"ChatGPT"`, `"React"`) rather than generic terms (`"AI"`, `"tech"`). Try multiple searches with different keywords.

---

## About PerfectPost

[PerfectPost](https://perfectpost.social) is a LinkedIn content management tool that helps you write, schedule, and analyze your posts. This skill exposes its full API through Claude Code via the Model Context Protocol (MCP).

---

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md).

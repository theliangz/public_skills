---
name: ai-news-daily
description: AI news aggregator and daily briefing tool. Automatically fetches latest AI industry news, model releases, technical reports from major AI news sites (aihot.today, ai-bot.cn) and web search. **Default behavior**: Display formatted daily AI news summary directly in conversation (titles, summaries, links). Optional: Send via email or write to Notion page when explicitly requested. Use when user requests today's AI news, latest AI model releases, AI industry events, or updates from major AI companies (Anthropic, Google, OpenAI, Alibaba Cloud, Zhipu, Moonshot, etc).
---

# AI News Daily

## Overview

Automatically collect latest AI industry news and compile into structured documents. Focus on model releases, technical reports, industry events, and updates from major AI companies.

**Default Behavior**: When invoked without specific output requirements, directly display the formatted AI news summary in the conversation (no email or Notion required).

## Workflow

### 0. Detect Output Mode (FIRST STEP)

Before fetching news, determine output method by checking user request:

1. **Email**: User mentions "email", "send to", "发送邮件", or provides email address
2. **Notion**: User mentions "notion", "write to notion", "上传notion", or provides Notion URL
3. **Direct Output**: No specific output method mentioned → Default to displaying in conversation

**Proceed with the appropriate workflow based on detected mode.**

### 1. Define News Scope

Default coverage:
- **Model Releases**: New model launches, updates, performance breakthroughs
- **Technical Reports**: Research papers, technical blogs, architecture updates
- **Industry Events**: Funding, acquisitions, partnerships, policy changes
- **Company Updates**: Anthropic, Google, OpenAI, Alibaba Cloud, Zhipu AI, Moonshot, Meta, Microsoft, etc.

### 2. News Sources

#### Primary Sources (fetch first)
1. **AIHot.today** - https://aihot.today/
2. **AI-Bot Daily AI News** - https://ai-bot.cn/daily-ai-news/

Use WebFetch or mcp__web_reader__webReader tools to fetch content from these sites.

#### Supplementary Sources (when needed)
Use WebSearch tool for latest news, keyword combinations:
- `{company} latest model release`
- `AI large language model today news`
- `{year} AI industry trends`

### 3. Content Extraction

From each source extract:
- **Title**: Complete news/event title
- **Summary**: 1-2 sentences capturing core content
- **Link**: Original article link
- **Time**: Publication time (if available)
- **Source**: Publishing company or media

### 4. Deduplication and Organization

- Sort by time (newest first)
- Merge duplicate reports of same event
- Group by category (Model Releases, Company Updates, Industry Events, etc.)

### 5. Output Format

#### Markdown Format (default)

```markdown
# AI Daily News - {date}

## Today's Summary
{Brief overview of key events}

## Model Releases
### [{Title}]({link})
**Summary**: {summary}
**Time**: {time}
**Company**: {company}

## Company Updates
### [{Company}]({link})
**Event**: {event description}
**Details**: {detail link}

## Industry Events
...

---
Sources: AIHot.today, AI-Bot, Web Search
Generated: {timestamp}
```

#### Email Format (optional)

If user provides email address, send via email. Subject: `AI Daily News - {date}`

## Output Methods

**IMPORTANT**: Always check which output method the user wants:

### Detection Logic (check in this order):
1. **Email**: If user mentions "email", "send to", "发送邮件", or provides email address → Use Email Delivery
2. **Notion**: If user mentions "notion", "write to notion", "上传notion", or provides Notion URL → Use Notion Integration
3. **Default (Direct Output)**: If no specific output method is mentioned → Display Markdown formatted news summary directly in conversation

### Output Methods:
1. **Default (Direct Output)**: Display Markdown formatted news summary directly in conversation - **This is the default behavior when no specific output method is requested**
2. **File Output**: Save as `.md` file if user explicitly requests it
3. **Email Delivery**: Send to provided email address (when user mentions email)
4. **Notion Integration**: Write to user's Notion page (when user mentions Notion, requires configuration)

### Notion Integration

When user provides a Notion page URL or requests Notion integration:

1. Ask user for Notion API credentials:
   - Integration Token (from https://www.notion.so/my-integrations)
   - Page ID (from the Notion page URL)

2. Use `scripts/notion_writer.py` to write formatted news to Notion

3. The script creates properly formatted Notion blocks:
   - Date headings
   - Callout blocks for summaries
   - Bullet list items for news entries
   - Proper links and formatting

Note: Notion API credentials are required. If user hasn't set up integration, guide them through:
- Creating an integration at notion.so/my-integrations
- Connecting the integration to their page
- Providing the API token and page ID

## Notes

- Verify link validity
- Ensure content freshness (prioritize today/yesterday content)
- Cite sources for traceability
- Avoid excessive marketing content
- Focus on technical substance over hype

## Example Triggers

### Direct Output (Default):
- "Get today's AI news" → Display in conversation
- "What's new in AI today" → Display in conversation
- "Latest AI model releases" → Display in conversation
- "What's new at Anthropic" → Display in conversation
- "AI industry today" → Display in conversation
- "今日AI资讯" → Display in conversation

### Email Delivery:
- "Send today's AI news to xxx@example.com"
- "Email me the AI news"
- "发送AI资讯到 xxx@example.com"

### Notion Integration:
- "Write AI news to my Notion page"
- "Upload to Notion"
- "上传AI资讯到Notion"

#!/usr/bin/env python3
"""
Notion Writer for AI News Daily
Writes formatted AI news to a Notion page using Notion API
"""

import requests
import sys
from datetime import datetime
from typing import List, Dict, Optional


class NotionWriter:
    """Write AI news to Notion page"""

    def __init__(self, api_token: str, page_id: str):
        """
        Initialize Notion writer

        Args:
            api_token: Notion Integration Token (starts with "secret_")
            page_id: Notion Page or Database ID
        """
        self.api_token = api_token
        self.page_id = page_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def append_to_page(self, blocks: List[Dict]) -> bool:
        """
        Append content blocks to a Notion page

        Args:
            blocks: List of Notion block objects

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/blocks/{self.page_id}/children"

        payload = {
            "children": blocks
        }

        try:
            response = requests.patch(url, json=payload, headers=self.headers)
            response.raise_for_status()
            print(f"Successfully appended {len(blocks)} blocks to Notion page")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error appending to Notion: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return False

    def create_date_heading(self, date_str: str) -> Dict:
        """Create a heading block with date"""
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": date_str}
                }]
            }
        }

    def create_divider(self) -> Dict:
        """Create a divider block"""
        return {
            "object": "block",
            "type": "divider",
            "divider": {}
        }

    def create_bullet(self, text: str) -> Dict:
        """Create a bullet list item block"""
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": text}
                }]
            }
        }

    def create_callout(self, text: str, emoji: str = "📰") -> Dict:
        """Create a callout block"""
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": text}
                }],
                "icon": {"emoji": emoji}
            }
        }

    def write_ai_news(self, news_data: Dict) -> bool:
        """
        Write formatted AI news to Notion

        Args:
            news_data: Dictionary containing:
                - date: News date string
                - summary: Today's summary
                - sections: List of news sections (Model Releases, Company Updates, etc.)

        Returns:
            True if successful, False otherwise
        """
        blocks = []

        # Date heading
        date_heading = self.create_date_heading(news_data.get("date", datetime.now().strftime("%Y年%m月%d日")))
        blocks.append(date_heading)

        # Divider
        blocks.append(self.create_divider())

        # Summary callout
        summary = news_data.get("summary", "")
        if summary:
            blocks.append(self.create_callout(f"**今日摘要**: {summary}"))

        # Add each section
        sections = news_data.get("sections", [])
        for section in sections:
            # Section heading
            section_title = section.get("title", "")
            if section_title:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": section_title}
                        }]
                    }
                })

            # Section items
            items = section.get("items", [])
            for item in items:
                title = item.get("title", "")
                link = item.get("link", "")
                summary_text = item.get("summary", "")
                company = item.get("company", "")
                time = item.get("time", "")

                # Format bullet item
                bullet_text = f"**{title}**"
                if link:
                    bullet_text += f" ([查看详情]({link}))"
                if summary_text:
                    bullet_text += f"\n{summary_text}"
                if company:
                    bullet_text += f"\n公司: {company}"
                if time:
                    bullet_text += f" | 时间: {time}"

                blocks.append(self.create_bullet(bullet_text))

        # Footer
        blocks.append(self.create_divider())
        blocks.append(self.create_bullet(f"Sources: AIHot.today, AI-Bot, Web Search | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"))

        # Append to page
        return self.append_to_page(blocks)


def main():
    """Main entry point for command line usage"""

    # Configuration - these would be provided by the user
    API_TOKEN = "secret_xxx"  # Replace with actual Notion Integration Token
    PAGE_ID = "xxx"  # Replace with actual Notion Page ID

    # Example news data structure
    news_data = {
        "date": "2026年2月28日",
        "summary": "Anthropic发布Claude Sonnet 4.6模型，智谱AI发布GLM-5，AI行业竞争加剧。",
        "sections": [
            {
                "title": "🚀 模型发布",
                "items": [
                    {
                        "title": "Anthropic发布Claude Sonnet 4.6",
                        "link": "https://example.com/link1",
                        "summary": "中端模型性能跃升，引发行业效率革命",
                        "company": "Anthropic",
                        "time": "2026年2月"
                    },
                    {
                        "title": "智谱GLM-5发布",
                        "link": "https://example.com/link2",
                        "summary": "千亿参数基座模型，推理速度提升40%",
                        "company": "智谱AI",
                        "time": "2026年2月"
                    }
                ]
            },
            {
                "title": "💰 融资动态",
                "items": [
                    {
                        "title": "OpenAI获得1100亿美元融资",
                        "link": "https://example.com/link3",
                        "summary": "新一轮融资完成",
                        "company": "OpenAI",
                        "time": "2026年2月"
                    }
                ]
            }
        ]
    }

    # Initialize writer and send
    writer = NotionWriter(API_TOKEN, PAGE_ID)
    success = writer.write_ai_news(news_data)

    if success:
        print("AI news successfully written to Notion!")
        sys.exit(0)
    else:
        print("Failed to write AI news to Notion")
        sys.exit(1)


if __name__ == "__main__":
    main()

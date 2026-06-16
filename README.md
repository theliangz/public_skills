# Public Skills

个人积累的 Claude Code / Claude Agent Skills 合集。每个 skill 是一个独立、即插即用的能力包，位于 `skills/` 目录下。

## 什么是 Skill

Skill 是 Claude（Claude Code、Claude Apps、Claude Agent SDK）的模块化能力扩展——一个包含 `SKILL.md`（描述 + 指令）以及可选 `references/`、`assets/`、`scripts/` 资源的文件夹。Claude 会根据用户请求自动匹配并加载对应 skill，无需手动配置。

> **安装**：将 `skills/` 下任意子目录复制到 `~/.claude/skills/`（用户级）或项目的 `.claude/skills/`（项目级）即可生效。

## Skills 一览

| Skill | 简介 | 触发场景 |
|-------|------|---------|
| [ai-news-daily](skills/ai-news-daily) | AI 行业新闻聚合与每日简报 | "今日 AI 资讯""最新模型发布" |
| [patent-writer](skills/patent-writer) | 专利申请文件自动撰写 | 撰写专利、技术交底书转专利文件 |
| [stock-analysis](skills/stock-analysis) | 综合股票分析与投资建议 | 股票筛选、投资建议、风险预警 |
| [ruankao-systemplan-tutor](skills/ruankao-systemplan-tutor) | 软考高级「系统规划与管理师」考试导师 | 系规考点讲解、真题解析、案例/论文辅导、备考规划 |

---

### 📰 ai-news-daily
AI 行业新闻聚合工具。自动从 AIHot.today、AI-Bot 等站点抓取最新 AI 资讯（模型发布、技术报告、行业事件、大厂动态），去重整理后输出结构化的每日简报。默认在对话中直接展示，也可按需发送邮件或写入 Notion。

**结构**：`SKILL.md` + `scripts/notion_writer.py`

### 📝 patent-writer
专业专利申请文件撰写工具。根据技术交底书、发明描述或技术资料，自动生成完整专利申请文件——权利要求书、说明书（技术领域 / 背景技术 / 发明内容 / 具体实施方式）、摘要等。支持发明专利与实用新型，含 2025 新规要点（强调实际解决效果、实施例与验证数据）。

**结构**：`SKILL.md` + `references/`（结构 / 权利要求 / 说明书指南）+ `assets/`（专利模板、交底书模板）

### 📈 stock-analysis
综合股票分析工具，支持短期（题材热点、技术指标 MACD/KDJ/RSI、资金流向、市场情绪）与长期（财务数据、行业前景、估值 PE/PB/DCF）两种策略，生成投资建议与风险预警。资讯来源覆盖同花顺、东方财富、中财网等。

> ⚠️ 分析仅供参考，不构成投资建议。

**结构**：`SKILL.md` + `references/`（技术指标 / 财务分析 / 风险评估）+ `assets/`（报告模板）+ `scripts/`（指标计算、新闻抓取、风险评估脚本）

### 🎓 ruankao-systemplan-tutor
软考高级「系统规划与管理师」考试专业导师。基于第 2 版教材（24 章 4 篇）与 2024 审定考纲，覆盖：综合知识选择题解析、案例分析答题（PPTR 四要素、IT 服务全生命周期、计算题）、IT 服务管理论文写作辅导、备考排期。内置命题规律分析与各章分值分布。

**结构**：`SKILL.md` + `references/`（考试概览 / 知识地图 / 案例分析 / 论文写作 / 备考策略）+ `assets/`（论文模板）

---

## 目录结构

```
public_skills/
├── README.md
└── skills/
    ├── ai-news-daily/            # 目录形式
    ├── patent-writer/            # 目录形式
    ├── stock-analysis/           # 目录形式
    └── ruankao-systemplan-tutor/ # 目录形式
```

## License
MIT

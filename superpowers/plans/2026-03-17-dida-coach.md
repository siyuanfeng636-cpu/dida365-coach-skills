# Dida Coach Skill 实施计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个结合滴答清单 MCP 的 Claude Code Skill，实现任务教练功能（目标拆解、时间盒子、复盘、情感支持）

**Architecture:** 单一 Skill 架构，内部模块化设计（Task/Coach/Review/Reminder/Closure 模块），通过滴答清单 MCP 进行任务读写，使用 Claude Code Cron 实现定时提醒

**Tech Stack:** YAML (skill 配置), Markdown (prompts), Python (工具脚本), 滴答清单 MCP API

---

## 文件结构规划

```
~/.claude/skills/dida-coach/
├── skill.yaml                      # Skill 入口定义
├── config.yaml                     # 默认配置
├── README.md                       # 使用说明
├── prompts/                        # Prompt 模板
│   ├── system.md                   # 系统角色设定
│   ├── setup.md                    # MCP 设置引导
│   ├── task_breakdown.md           # 任务拆解流程
│   ├── timebox_creation.md         # 时间盒子创建
│   ├── checkpoint.md               # 检查点确认
│   ├── rescheduling.md             # 改时间处理
│   ├── daily_review.md             # 日复盘
│   ├── weekly_review.md            # 周复盘
│   └── coach_personas/             # 各文风预设
│       ├── warm_encouraging.md
│       ├── strict_coach.md
│       ├── rational_analyst.md
│       └── humorous.md
└── tools/                          # 工具脚本
    ├── __init__.py
    ├── mcp_client.py               # MCP 客户端封装
    ├── config_manager.py           # 配置管理
    ├── task_parser.py              # 任务解析
    ├── timebox_calculator.py       # 时间盒计算
    ├── work_method_recommender.py  # 工作法推荐
    └── review_analyzer.py          # 复盘分析
```

---

## Chunk 1: 基础结构和 MCP 连接检测

### Task 1: 创建 Skill 基础结构

**Files:**
- Create: `~/.claude/skills/dida-coach/skill.yaml`
- Create: `~/.claude/skills/dida-coach/README.md`

- [ ] **Step 1: 创建 skill.yaml**

```yaml
name: dida-coach
description: 滴答清单任务教练 - 帮你拆解目标、管理时间盒子、定期复盘
version: 1.0.0
author: openclaw

setup:
  required_mcp:
    - name: dida365
      url: https://mcp.dida365.com
      description: 滴答清单 MCP，用于任务读写

entry_points:
  default:
    prompt: prompts/system.md
    tools:
      - tools.mcp_client
      - tools.config_manager
      - tools.task_parser
      - tools.timebox_calculator
      - tools.work_method_recommender
      - tools.review_analyzer
```

- [ ] **Step 2: 创建 README.md**

```markdown
# Dida Coach - 滴答清单任务教练

你的 AI 任务管理伙伴，帮你：
- 🎯 把大目标拆解成可执行的小任务
- ⏱️ 用时间盒子高效专注
- 📊 定期复盘，持续改进
- 💪 情感支持，告别拖延

## 安装

1. 确保已安装滴答清单 MCP：
   ```bash
   claude mcp add --transport http dida365 https://mcp.dida365.com
   ```

2. 运行 `/mcp` 完成授权

3. 使用本 skill

## 使用示例

- "我想提高英语口语" → 目标拆解
- "我要写一份报告" → 创建时间盒子
- "复盘今天/这周" → 自动复盘
- "早上好" → 今日计划
```

- [ ] **Step 3: 提交**

```bash
cd ~/.claude/skills/dida-coach
git init
git add skill.yaml README.md
git commit -m "feat: initialize dida-coach skill structure"
```

---

### Task 2: MCP 连接检测工具

**Files:**
- Create: `~/.claude/skills/dida-coach/tools/__init__.py`
- Create: `~/.claude/skills/dida-coach/tools/mcp_client.py`

- [ ] **Step 1: 创建 tools/__init__.py**

```python
"""Dida Coach tools package."""
```

- [ ] **Step 2: 创建 MCP 检测函数（TDD：先写测试）**

在 `~/.claude/skills/dida-coach/tools/mcp_client.py` 中：

```python
"""MCP 客户端工具 - 处理与滴答清单的连接和数据交互."""

import json
import os
from typing import Dict, List, Optional, Tuple


def check_mcp_configured() -> Tuple[bool, str]:
    """
    检查滴答清单 MCP 是否已配置.

    Returns:
        (是否配置, 提示信息)
    """
    mcp_config_path = os.path.expanduser("~/.claude/mcp.json")

    if not os.path.exists(mcp_config_path):
        return False, """
👋 欢迎使用 Dida Coach！

检测到您尚未连接滴答清单，请先执行以下步骤：

1. 运行：claude mcp add --transport http dida365 https://mcp.dida365.com
2. 然后运行：/mcp
3. 按提示完成滴答清单授权

完成后我会自动检测连接。
"""

    try:
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)

        # 检查是否有 dida365 配置
        if 'mcpServers' in config and 'dida365' in config['mcpServers']:
            return True, "✅ 滴答清单 MCP 已配置"

        # 检查新版格式
        if 'servers' in config and 'dida365' in config['servers']:
            return True, "✅ 滴答清单 MCP 已配置"

        return False, """
👋 检测到 MCP 配置文件，但未找到 dida365 配置。

请运行：claude mcp add --transport http dida365 https://mcp.dida365.com
然后运行 /mcp 完成授权。
"""
    except (json.JSONDecodeError, IOError) as e:
        return False, f"❌ 读取 MCP 配置失败: {e}"


def get_mcp_setup_command() -> str:
    """获取 MCP 设置命令."""
    return "claude mcp add --transport http dida365 https://mcp.dida365.com"
```

- [ ] **Step 3: 验证 MCP 检测工具**

测试方式：在 Python REPL 中

```python
import sys
sys.path.insert(0, '~/.claude/skills/dida-coach')
from tools.mcp_client import check_mcp_configured

# 测试：应该根据实际配置返回结果
result, msg = check_mcp_configured()
print(f"Configured: {result}")
print(f"Message: {msg}")
```

- [ ] **Step 4: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add tools/__init__.py tools/mcp_client.py
git commit -m "feat: add MCP connection detection"
```

---

### Task 3: 系统 Prompt 和设置引导

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/system.md`
- Create: `~/.claude/skills/dida-coach/prompts/setup.md`

- [ ] **Step 1: 创建 system.md**

```markdown
# Dida Coach 系统角色

你是用户的任务管理教练，结合滴答清单 MCP 帮助用户高效管理任务。

## 核心职责

1. **目标拆解**：帮用户把大目标拆解成可执行的阶段性任务
2. **时间盒子**：创建 30 分钟为单位的时间盒子，确保每个盒子有明确成果
3. **闭环反馈**：定期检查任务进展，完成时庆祝，未完成时提供支持
4. **定期复盘**：日复盘（21:00）和周复盘（周日 20:00）
5. **情感支持**：根据用户设定的文风，提供激励和 accountability

## 工作流程

### 首次使用
1. 调用 `check_mcp_configured()` 检查 MCP 配置
2. 如未配置，显示 setup.md 中的引导
3. 如已配置，询问用户主要需求

### 日常交互
- 识别用户意图（目标拆解/时间盒子/复盘/改时间）
- 调用相应模块处理
- 通过 MCP 读写滴答清单任务
- 使用 Cron 设置提醒

## 文风设定

根据 config.yaml 中的 personality.preset 加载对应文风：
- warm_encouraging: 温暖鼓励型
- strict_coach: 严格教练型
- rational_analyst: 理性分析型
- humorous: 幽默调侃型

## 重要约束

- 时间盒子默认 30 分钟，连续 4 个后长休息 15 分钟
- 每个盒子必须有明确的成果检查点
- 未完成时先共情/理解，再提供解决方案
- 复盘数据按需存入 memory，重复模式进长期记忆
```

- [ ] **Step 2: 创建 setup.md**

```markdown
# 滴答清单 MCP 设置引导

👋 欢迎使用 Dida Coach！

检测到您尚未连接滴答清单，请按以下步骤操作：

## 第一步：添加 MCP

在终端运行：
```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

## 第二步：授权

在 Claude Code 中运行：
```
/mcp
```

按提示完成滴答清单的 OAuth 授权。

## 第三步：验证

授权完成后，告诉我"已连接"，我会自动检测并进入主菜单。

---

**常见问题：**

Q: 授权页面打不开？
A: 请检查网络连接，或尝试复制链接到浏览器手动打开。

Q: 提示"已配置"但无法使用？
A: 运行 `/mcp` 检查连接状态，可能需要重新授权。
```

- [ ] **Step 3: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/system.md prompts/setup.md
git commit -m "feat: add system prompt and setup guide"
```

---

## Chunk 2: 配置管理模块

### Task 4: 配置管理工具

**Files:**
- Create: `~/.claude/skills/dida-coach/tools/config_manager.py`
- Create: `~/.claude/skills/dida-coach/config.yaml`

- [ ] **Step 1: 创建默认 config.yaml**

```yaml
# Dida Coach 默认配置

# 文风设定
personality:
  preset: "warm_encouraging"  # 可选: strict_coach / rational_analyst / humorous / custom

# 工作法配置
work_method:
  default: "flexible_pomodoro"
  auto_recommend: true  # 根据任务类型智能推荐

  methods:
    flexible_pomodoro:
      name: "灵活番茄（默认）"
      focus: 30
      short_break: 5
      long_break: 15
      boxes_before_long: 4
      max_consecutive: 4

    classic_pomodoro:
      name: "经典番茄"
      focus: 25
      short_break: 5
      long_break: 15
      boxes_before_long: 4
      max_consecutive: 4

    long_pomodoro:
      name: "长番茄（深度工作）"
      focus: 50
      short_break: 10
      long_break: 30
      boxes_before_long: 2
      max_consecutive: 2

    ultradian:
      name: "90分钟深度"
      focus: 90
      short_break: 0
      long_break: 20
      boxes_before_long: 1
      max_consecutive: 1

# 提醒时间
reminders:
  daily_plan: "09:00"
  daily_review: "21:00"
  weekly_review: "Sunday 20:00"
  enabled: true

# 复盘维度
review:
  dimensions:
    - completion_rate
    - time_distribution
    - task_type_analysis
    - missed_reason
    - suggestions
    - highlights
    - procrastination_time
    - automation_candidates

# 闭环设置
closure:
  check_in_enabled: true
  missed_task_follow_up: true
  max_reschedule_times: 3
```

- [ ] **Step 2: 创建 config_manager.py**

```python
"""配置管理工具."""

import os
import yaml
from typing import Dict, Any, Optional

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
USER_CONFIG_PATH = os.path.expanduser('~/.claude/skills/dida-coach/config.yaml')


def load_config() -> Dict[str, Any]:
    """
    加载配置，优先使用用户配置，缺失项使用默认配置.

    Returns:
        合并后的配置字典
    """
    # 加载默认配置
    with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 加载用户配置并合并
    if os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
        if user_config:
            _deep_merge(config, user_config)

    return config


def _deep_merge(base: Dict, override: Dict) -> None:
    """深度合并字典."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_personality_preset(config: Dict) -> str:
    """获取当前文风预设."""
    return config.get('personality', {}).get('preset', 'warm_encouraging')


def get_work_method_config(config: Dict, method_name: Optional[str] = None) -> Dict:
    """获取工作法配置."""
    methods = config.get('work_method', {}).get('methods', {})
    if method_name:
        return methods.get(method_name, methods.get('flexible_pomodoro', {}))

    default = config.get('work_method', {}).get('default', 'flexible_pomodoro')
    return methods.get(default, {})


def get_reminder_config(config: Dict) -> Dict:
    """获取提醒配置."""
    return config.get('reminders', {})


def save_user_config(updates: Dict[str, Any]) -> None:
    """保存用户配置更新."""
    config = {}
    if os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

    _deep_merge(config, updates)

    os.makedirs(os.path.dirname(USER_CONFIG_PATH), exist_ok=True)
    with open(USER_CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
```

- [ ] **Step 3: 验证配置管理**

```python
import sys
sys.path.insert(0, '~/.claude/skills/dida-coach')
from tools.config_manager import load_config, get_personality_preset, get_work_method_config

config = load_config()
print(f"Preset: {get_personality_preset(config)}")
print(f"Work method: {get_work_method_config(config)}")
```

- [ ] **Step 4: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add config.yaml tools/config_manager.py
git commit -m "feat: add configuration management"
```

---

## Chunk 3: 任务拆解模块

### Task 5: 任务解析工具

**Files:**
- Create: `~/.claude/skills/dida-coach/tools/task_parser.py`

- [ ] **Step 1: 创建任务解析工具**

```python
"""任务解析工具 - 解析用户输入，生成结构化任务数据."""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


def parse_goal_input(text: str) -> Dict:
    """
    解析用户的目标描述，提取关键信息.

    Args:
        text: 用户输入，如"我想提高英语口语"

    Returns:
        解析结果字典
    """
    result = {
        'raw_input': text,
        'goal_type': None,  # skill, habit, project
        'domain': None,     # 领域：语言、技能、健康等
        'time_commitment': None,  # 时间投入
    }

    # 识别目标类型
    skill_keywords = ['学', '提高', '掌握', '练习', '提升']
    habit_keywords = ['养成', '每天', '坚持', '打卡']
    project_keywords = ['完成', '准备', '项目', '报告', '论文']

    text_lower = text.lower()
    if any(k in text_lower for k in skill_keywords):
        result['goal_type'] = 'skill'
    elif any(k in text_lower for k in habit_keywords):
        result['goal_type'] = 'habit'
    elif any(k in text_lower for k in project_keywords):
        result['goal_type'] = 'project'

    # 识别领域
    domains = {
        'language': ['英语', '日语', '法语', '语言', '口语', '听力'],
        'fitness': ['健身', '跑步', '运动', '减肥', '锻炼'],
        'career': ['工作', '职业', '升职', '面试', '技能'],
        'study': ['学习', '考试', '考证', '读书'],
    }

    for domain, keywords in domains.items():
        if any(k in text for k in keywords):
            result['domain'] = domain
            break

    return result


def parse_timebox_input(text: str) -> Dict:
    """
    解析时间盒子创建请求.

    Args:
        text: 如"我明天要完成报告"

    Returns:
        解析结果
    """
    result = {
        'raw_input': text,
        'task_description': None,
        'deadline': None,
        'estimated_duration': None,  # 预估时长（分钟）
    }

    # 提取任务描述
    # 移除时间词，保留核心任务
    time_patterns = [
        r'今天', r'明天', r'后天',
        r'下周[一二三四五六日]?',
        r'[上下]午', r'晚上?',
        r'[\d]+点',
    ]

    desc = text
    for pattern in time_patterns:
        desc = re.sub(pattern, '', desc)

    # 清理
    desc = re.sub(r'[我要准备想把]', '', desc).strip()
    result['task_description'] = desc

    # 判断预估时长
    project_keywords = ['报告', '论文', '项目', '方案', 'PPT', '文档']
    quick_keywords = ['邮件', '电话', '回复', '确认', '打卡']

    if any(k in text for k in project_keywords):
        result['estimated_duration'] = 120  # 2小时
    elif any(k in text for k in quick_keywords):
        result['estimated_duration'] = 30   # 30分钟
    else:
        result['estimated_duration'] = 60   # 默认1小时

    return result


def extract_priority(text: str) -> Optional[str]:
    """从文本中提取优先级."""
    if '!1' in text or '高优先级' in text or '重要' in text:
        return 'high'
    elif '!2' in text or '中优先级' in text:
        return 'medium'
    elif '!3' in text or '低优先级' in text:
        return 'low'
    return None


def extract_tags(text: str) -> List[str]:
    """从文本中提取标签 (#标签)."""
    tags = re.findall(r'#([^\s#]+)', text)
    return tags


def parse_reschedule_request(text: str) -> Dict:
    """
    解析改时间请求.

    Args:
        text: 如"把盒子 2 改到下午 2 点"

    Returns:
        改时间参数
    """
    result = {
        'box_number': None,  # None 表示全部
        'new_time': None,
        'adjustment': None,  # delay_1h, advance_30m 等
    }

    # 提取盒子编号
    box_match = re.search(r'盒子\s*(\d+)', text)
    if box_match:
        result['box_number'] = int(box_match.group(1))

    # 识别改时间模式
    if '延后' in text or '推迟' in text or '延后' in text:
        time_match = re.search(r'(\d+)\s*小时', text)
        if time_match:
            result['adjustment'] = f"delay_{time_match.group(1)}h"

    if '提前' in text:
        time_match = re.search(r'(\d+)\s*小时', text)
        if time_match:
            result['adjustment'] = f"advance_{time_match.group(1)}h"

    return result
```

- [ ] **Step 2: 验证任务解析**

```python
import sys
sys.path.insert(0, '~/.claude/skills/dida-coach')
from tools.task_parser import parse_goal_input, parse_timebox_input

# 测试目标解析
result = parse_goal_input("我想提高英语口语")
print(f"Goal parse: {result}")

# 测试时间盒解析
result = parse_timebox_input("我明天要完成报告")
print(f"Timebox parse: {result}")
```

- [ ] **Step 3: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add tools/task_parser.py
git commit -m "feat: add task parsing utilities"
```

---

### Task 6: 任务拆解 Prompt

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/task_breakdown.md`

- [ ] **Step 1: 创建 task_breakdown.md**

```markdown
# 任务拆解流程

## 目标
帮用户把大目标拆解成可执行的阶段性任务，并创建到滴答清单。

## 流程

### Step 1: 了解背景（最多 3 个问题）

用户说了一个目标后，按顺序询问：

1. **当前水平**（针对技能类）
   - A. 零基础/刚开始
   - B. 有基础，想提升
   - C. 比较熟练，想精通

2. **时间投入**
   - "每周能投入多少时间？"
   - 或给出选项：A. 每天15分钟 B. 每天30分钟 C. 每天1小时 D. 更多

3. **具体场景**（可选）
   - 学英语：工作/留学/旅行/兴趣？
   - 健身：减脂/增肌/健康/比赛？

### Step 2: 生成阶段性计划

基于用户情况，生成 3 个阶段的计划：

```
🎯 第1月：[阶段主题]（每日 [X] 分钟）
   • [具体任务1]
   • [具体任务2]
   • [具体任务3]

🎯 第2月：[阶段主题]（每日 [X] 分钟）
   ...

🎯 第3月：[阶段主题]（每日 [X] 分钟）
   ...
```

### Step 3: 确认并创建

询问："需要我把这个计划创建到滴答清单吗？我会：
- 创建'[目标名称]'清单
- 每月一个任务，包含每日子任务
- 设置合适的提醒"

用户确认后，调用 MCP 创建：
- 清单：[目标名称]
- 任务1：[第1月主题] !2 #习惯养成
  - 子任务：Day 1-30 的具体任务
- 任务2：[第2月主题] !2
- 任务3：[第3月主题] !2

### Step 4: 设置检查点

"计划已创建！我会在每周末询问你这周的执行情况，方便吗？"
```

- [ ] **Step 2: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/task_breakdown.md
git commit -m "feat: add task breakdown prompt"
```

---

## Chunk 4: 时间盒子模块

### Task 7: 时间盒计算工具

**Files:**
- Create: `~/.claude/skills/dida-coach/tools/timebox_calculator.py`
- Create: `~/.claude/skills/dida-coach/tools/work_method_recommender.py`

- [ ] **Step 1: 创建时间盒计算工具**

```python
"""时间盒子计算工具 - 计算时间盒安排."""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


def calculate_timeboxes(
    task_description: str,
    estimated_minutes: int,
    start_time: datetime,
    work_method: Dict
) -> List[Dict]:
    """
    计算时间盒子安排.

    Args:
        task_description: 任务描述
        estimated_minutes: 预估总时长（分钟）
        start_time: 开始时间
        work_method: 工作法配置

    Returns:
        时间盒子列表
    """
    focus_time = work_method.get('focus', 30)
    short_break = work_method.get('short_break', 5)
    long_break = work_method.get('long_break', 15)
    boxes_before_long = work_method.get('boxes_before_long', 4)

    # 计算需要几个盒子
    num_boxes = max(1, (estimated_minutes + focus_time - 1) // focus_time)

    boxes = []
    current_time = start_time

    for i in range(num_boxes):
        box_num = i + 1

        # 计算开始和结束时间
        box_start = current_time
        box_end = box_start + timedelta(minutes=focus_time)

        # 生成果果描述
        deliverable = generate_deliverable(task_description, box_num, num_boxes)

        box = {
            'number': box_num,
            'start_time': box_start,
            'end_time': box_end,
            'focus_minutes': focus_time,
            'deliverable': deliverable,
            'task_title': f"📦 盒子 {box_num}: {task_description[:20]}...",
        }
        boxes.append(box)

        # 计算下一个盒子的开始时间（含休息）
        if i < num_boxes - 1:  # 不是最后一个盒子
            if box_num % boxes_before_long == 0:
                # 长休息
                current_time = box_end + timedelta(minutes=long_break)
            else:
                # 短休息
                current_time = box_end + timedelta(minutes=short_break)

    return boxes


def generate_deliverable(task: str, box_num: int, total_boxes: int) -> str:
    """根据任务类型和盒子序号，生成应完成的成果描述."""

    # 常见任务类型的拆分模板
    templates = {
        '报告': {
            1: '完成背景介绍和现状概述',
            2: '梳理问题清单',
            3: '给出解决方案',
            4: '整合完整报告',
        },
        '写作': {
            1: '完成大纲和开头',
            2: '完成主体第一部分',
            3: '完成主体第二部分',
            4: '完成结尾和润色',
        },
        '代码': {
            1: '完成核心逻辑框架',
            2: '实现主要功能',
            3: '处理边界情况',
            4: '测试和优化',
        },
        '学习': {
            1: '通读材料，标记重点',
            2: '整理笔记和框架',
            3: '深入理解难点',
            4: '总结和应用',
        },
    }

    # 匹配任务类型
    for keyword, template in templates.items():
        if keyword in task:
            return template.get(box_num, f'完成第 {box_num}/{total_boxes} 部分')

    # 默认拆分
    if total_boxes == 1:
        return f'完成{task}'
    elif box_num == 1:
        return f'完成框架和第一部分'
    elif box_num == total_boxes:
        return f'完成最后部分和整理'
    else:
        return f'完成第 {box_num}/{total_boxes} 部分'


def format_timebox_schedule(boxes: List[Dict]) -> str:
    """格式化时间盒安排为可读字符串."""
    lines = []

    for box in boxes:
        start = box['start_time'].strftime('%H:%M')
        end = box['end_time'].strftime('%H:%M')

        lines.append(f"📦 盒子 {box['number']} | {start}-{end} | 成果：{box['deliverable']} ✓")
        lines.append(f"   └─ {box['task_title']}")
        lines.append("")

    return '\n'.join(lines)


def reschedule_boxes(
    boxes: List[Dict],
    box_number: Optional[int] = None,
    new_start_time: Optional[datetime] = None,
    adjustment_minutes: Optional[int] = None
) -> List[Dict]:
    """
    重新安排时间盒.

    Args:
        boxes: 原时间盒列表
        box_number: 要改的盒子编号（None 表示全部）
        new_start_time: 新的开始时间
        adjustment_minutes: 调整分钟数（正数延后，负数提前）

    Returns:
        新的时间盒列表
    """
    if not boxes:
        return boxes

    # 计算时间偏移
    if adjustment_minutes is not None:
        offset = timedelta(minutes=adjustment_minutes)
    elif new_start_time is not None:
        offset = new_start_time - boxes[0]['start_time']
    else:
        return boxes

    # 如果只改某个盒子，从该盒子开始调整
    start_index = (box_number - 1) if box_number else 0

    for i in range(start_index, len(boxes)):
        boxes[i]['start_time'] += offset
        boxes[i]['end_time'] += offset

    return boxes
```

- [ ] **Step 2: 创建工作法推荐工具**

```python
"""工作法推荐工具 - 根据任务类型推荐最佳工作法."""

from typing import Dict, Optional


# 任务类型到工作法的映射
TASK_TYPE_MAPPING = {
    # 深度工作
    '编程': 'long_pomodoro',
    '代码': 'long_pomodoro',
    '写作': 'long_pomodoro',
    '设计': 'long_pomodoro',
    '论文': 'ultradian',
    '报告': 'flexible_pomodoro',

    # 沟通类
    '邮件': 'flexible_pomodoro',
    '回复': 'flexible_pomodoro',
    '沟通': 'flexible_pomodoro',
    '会议': 'flexible_pomodoro',

    # 学习类
    '学习': 'flexible_pomodoro',
    '阅读': 'flexible_pomodoro',
    '笔记': 'flexible_pomodoro',

    # 创意类
    '头脑风暴': 'ultradian',
    '创意': 'ultradian',
    '策划': 'long_pomodoro',

    # 事务类
    '整理': 'classic_pomodoro',
    '归档': 'classic_pomodoro',
    '数据': 'flexible_pomodoro',
}


def recommend_work_method(task_description: str) -> str:
    """
    根据任务描述推荐工作法.

    Args:
        task_description: 任务描述

    Returns:
        工作法名称
    """
    task_lower = task_description.lower()

    for keyword, method in TASK_TYPE_MAPPING.items():
        if keyword in task_lower:
            return method

    # 默认返回灵活番茄
    return 'flexible_pomodoro'


def get_work_method_reasoning(task_description: str, method: str) -> str:
    """获取推荐工作法的理由."""

    reasonings = {
        'flexible_pomodoro': '这个任务适合 30 分钟的节奏，既能保持专注，又便于调整。',
        'classic_pomodoro': '这个任务适合经典番茄（25分钟），快速迭代，适合碎片化处理。',
        'long_pomodoro': '这是深度工作类型，建议用 50 分钟长番茄，减少上下文切换，更容易进入心流。',
        'ultradian': '这个任务需要长时间专注和创意，建议用 90 分钟深度模式，给大脑充分的时间进入状态。',
    }

    return reasonings.get(method, reasonings['flexible_pomodoro'])


def explain_work_method(method: str, config: Dict) -> str:
    """解释工作法的具体参数."""

    method_config = config.get('work_method', {}).get('methods', {}).get(method, {})

    if not method_config:
        return "使用默认配置"

    name = method_config.get('name', method)
    focus = method_config.get('focus', 30)
    short_break = method_config.get('short_break', 5)
    long_break = method_config.get('long_break', 15)
    boxes_before_long = method_config.get('boxes_before_long', 4)

    return (
        f"**{name}**：专注 {focus} 分钟，"
        f"短休息 {short_break} 分钟，"
        f"每 {boxes_before_long} 个盒子后长休息 {long_break} 分钟"
    )
```

- [ ] **Step 3: 验证时间盒计算**

```python
import sys
from datetime import datetime
sys.path.insert(0, '~/.claude/skills/dida-coach')
from tools.timebox_calculator import calculate_timeboxes, format_timebox_schedule
from tools.config_manager import load_config, get_work_method_config

config = load_config()
method = get_work_method_config(config)

start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
boxes = calculate_timeboxes("写项目报告", 120, start, method)

print(format_timebox_schedule(boxes))
```

- [ ] **Step 4: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add tools/timebox_calculator.py tools/work_method_recommender.py
git commit -m "feat: add timebox calculation and work method recommendation"
```

---

### Task 8: 时间盒子相关 Prompts

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/timebox_creation.md`
- Create: `~/.claude/skills/dida-coach/prompts/checkpoint.md`
- Create: `~/.claude/skills/dida-coach/prompts/rescheduling.md`

- [ ] **Step 1: 创建 timebox_creation.md**

```markdown
# 时间盒子创建流程

## 目标
帮用户创建时间盒子，将大任务拆分为 30 分钟（或选定工作法）的专注时段。

## 流程

### Step 1: 了解任务

用户说要做某事时，询问：
1. 任务具体内容（如果描述不清晰）
2. "预计需要多长时间完成？"
   或给出选项：A. 30分钟 B. 1小时 C. 2小时 D. 更久

### Step 2: 推荐工作法

根据任务类型，调用 recommend_work_method()，并说明理由：

"这个任务建议用 **长番茄模式（50分钟）**，因为写代码需要深度专注，减少上下文切换。

工作法对比：
- A. 长番茄（50分钟）- 适合深度工作 ⭐ 推荐
- B. 灵活番茄（30分钟）- 适合快速迭代
- C. 90分钟深度 - 适合创意构思

你想用哪种？"

### Step 3: 生成时间盒安排

调用 calculate_timeboxes() 生成安排，展示给用户：

"建议拆分为 4 个时间盒子（2小时）：

📦 盒子 1 | 09:00-09:30 | 成果：进度框架 ✓
   └─ 完成项目背景 + 当前进度概述

📦 盒子 2 | 09:35-10:05 | 成果：问题清单 ✓
   └─ 梳理遇到的问题及原因

📦 盒子 3 | 10:10-10:40 | 成果：解决方案 ✓
   └─ 针对问题给出解决方案

📦 盒子 4 | 10:45-11:15 | 成果：完整报告 ✓
   └─ 整合 + 下阶段计划 + 格式美化

🔄 长休息 11:15-11:30

需要调整吗？你可以：
• 说'改成 45 分钟'调整时长
• 说'下午开始'改时间
• 说'删除盒子 3'简化任务"

### Step 4: 确认并创建

用户确认后：
1. 调用 MCP 创建任务（每个盒子一个任务）
2. 设置标题格式："📦 盒子 N: [内容]"
3. 在描述中写明预期成果
4. 设置截止时间
5. 添加标签 #时间盒子 #[工作法名称]

### Step 5: 设置检查点提醒

"已创建到滴答清单！我会在每个盒子结束时提醒你确认成果。

第一个检查点：[时间]，到时候我会问你进展如何。"

使用 CronCreate 设置提醒：
- 每个盒子结束时间触发
- prompt: "检查盒子 N 完成情况"
```

- [ ] **Step 2: 创建 checkpoint.md**

```markdown
# 检查点确认流程

## 触发条件
- Cron 定时触发（盒子结束时间）
- 用户主动说"检查点"或"盒子 X 完成"

## 确认流程

### 显示检查点信息

```
⏰ 时间到！盒子 [N] 结束 ([时间])

📋 应完成成果：[deliverable]

✅ 实际完成度？
A. 100% - 按计划完成，可以进入下一盒
B. 80% - 基本完成，小尾巴下一盒补
C. 50% - 需要延长 10 分钟
D. 没做完 - 遇到什么问题？
```

### 根据选择处理

**选择 A/B：庆祝并进入下一盒**
- 根据文风给予鼓励
- 提醒休息时间和下一盒开始时间
- 更新滴答清单任务状态

**选择 C：延长当前盒子**
- 确认延长到几点
- 更新提醒时间
- 鼓励："专注完成比按时完成更重要"

**选择 D：询问原因并提供支持**
- 询问："是任务比预想的难，还是分心了？"
- 根据原因：
  - 太难 → "需要我帮你进一步拆解吗？"
  - 分心 → "建议把手机放远点，开启专注模式"
  - 没动力 → "想想完成这个汇报后你会有什么收获？"
- 重新约定完成时间
- 更新任务并设置新检查点

### 记录闭环

在滴答清单任务备注中记录：
- 实际完成度
- 原因（如果未完成）
- 调整后的计划
```

- [ ] **Step 3: 创建 rescheduling.md**

```markdown
# 改时间处理流程

## 支持的改时间请求

### 1. 改单个盒子
"把盒子 2 改到下午 2 点"

处理：
1. 调用 reschedule_boxes(box_number=2, new_start_time=14:00)
2. 更新滴答清单中该任务的截止时间
3. 更新 Cron 提醒时间
4. 确认："盒子 2 已改到 14:00-14:30，后续盒子自动顺延"

### 2. 批量延后
"所有盒子延后 1 小时"

处理：
1. 调用 reschedule_boxes(adjustment_minutes=60)
2. 批量更新所有任务和提醒
3. 展示新的时间安排

### 3. 改时长
"盒子 3 改到 45 分钟"

处理：
1. 重新计算该盒子结束时间
2. 后续盒子自动顺延
3. 更新任务和提醒

### 4. 取消全部
"今天状态不好，全部取消"

处理：
1. 询问原因："是身体不舒服还是有其他安排？"
2. 询问改期："需要改到明天吗？"
3. 根据回答：
   - 改期 → 批量 reschedule
   - 取消 → 删除滴答清单任务，记录原因到 memory
4. 给予支持（根据文风）：
   - 温暖型："没关系，休息好更重要。明天再战！"
   - 严格型："这次算了，但不要养成逃避的习惯。"

## 改时间后的同步

每次改时间后需要更新：
1. 滴答清单任务截止时间
2. Cron 提醒时间（删除旧的，创建新的）
3. 本地时间盒数据
```

- [ ] **Step 4: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/timebox_creation.md prompts/checkpoint.md prompts/rescheduling.md
git commit -m "feat: add timebox creation, checkpoint and rescheduling prompts"
```

---

## Chunk 5: 复盘模块

### Task 9: 复盘分析工具

**Files:**
- Create: `~/.claude/skills/dida-coach/tools/review_analyzer.py`

- [ ] **Step 1: 创建复盘分析工具**

```python
"""复盘分析工具 - 分析任务数据，生成复盘报告."""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict


def analyze_daily_tasks(tasks: List[Dict]) -> Dict:
    """
    分析单日任务数据.

    Args:
        tasks: 滴答清单任务列表

    Returns:
        分析结果
    """
    if not tasks:
        return {'total': 0, 'completed': 0, 'completion_rate': 0}

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get('status') == 'completed')

    # 按小时统计完成情况（用于找高效时段）
    hour_distribution = defaultdict(lambda: {'completed': 0, 'total': 0})

    for task in tasks:
        # 从任务时间提取小时
        task_time = task.get('due_date') or task.get('start_date')
        if task_time:
            hour = datetime.fromisoformat(task_time).hour
            hour_distribution[hour]['total'] += 1
            if task.get('status') == 'completed':
                hour_distribution[hour]['completed'] += 1

    # 找最高效时段
    peak_hours = sorted(
        hour_distribution.items(),
        key=lambda x: x[1]['completed'] / max(x[1]['total'], 1),
        reverse=True
    )[:2]

    # 任务类型分布
    type_distribution = defaultdict(int)
    for task in tasks:
        tags = task.get('tags', [])
        if '工作' in tags or 'work' in tags:
            type_distribution['work'] += 1
        elif '学习' in tags or 'study' in tags:
            type_distribution['study'] += 1
        elif '生活' in tags or 'life' in tags:
            type_distribution['life'] += 1
        else:
            type_distribution['other'] += 1

    return {
        'total': total,
        'completed': completed,
        'completion_rate': round(completed / total * 100, 1) if total > 0 else 0,
        'peak_hours': [f"{h[0]}:00-{h[0]+1}:00" for h in peak_hours if h[1]['total'] > 0],
        'type_distribution': dict(type_distribution),
    }


def analyze_weekly_trends(daily_stats: List[Dict]) -> Dict:
    """
    分析一周趋势.

    Args:
        daily_stats: 每日统计数据列表

    Returns:
        趋势分析结果
    """
    if not daily_stats:
        return {}

    completion_rates = [d['completion_rate'] for d in daily_stats]
    avg_rate = sum(completion_rates) / len(completion_rates)

    # 找最 productive 的一天
    best_day = max(daily_stats, key=lambda x: x['completion_rate'])
    worst_day = min(daily_stats, key=lambda x: x['completion_rate'])

    # 趋势（上升/下降/平稳）
    first_half = sum(completion_rates[:len(completion_rates)//2]) / (len(completion_rates)//2 or 1)
    second_half = sum(completion_rates[len(completion_rates)//2:]) / (len(completion_rates) - len(completion_rates)//2 or 1)

    if second_half > first_half + 10:
        trend = '上升 📈'
    elif second_half < first_half - 10:
        trend = '下降 📉'
    else:
        trend = '平稳 ➡️'

    return {
        'average_completion_rate': round(avg_rate, 1),
        'best_day': best_day,
        'worst_day': worst_day,
        'trend': trend,
        'daily_rates': completion_rates,
    }


def identify_missed_patterns(missed_tasks: List[Dict]) -> List[Dict]:
    """
    识别未完成任务的规律.

    Args:
        missed_tasks: 未完成的任务列表

    Returns:
        识别的模式
    """
    patterns = []

    if not missed_tasks:
        return patterns

    # 按任务名分组，看是否有重复未完成的
    task_names = defaultdict(int)
    for task in missed_tasks:
        # 简化任务名（去掉日期等）
        name = task.get('title', '').split(' ')[0]
        task_names[name] += 1

    # 找出重复未完成的
    recurring_missed = [(name, count) for name, count in task_names.items() if count >= 2]
    if recurring_missed:
        patterns.append({
            'type': 'recurring_missed',
            'description': f"重复未完成: {', '.join([f'{n}({c}次)' for n, c in recurring_missed])}",
            'suggestion': '建议进一步拆解或调整优先级',
        })

    # 按时间段分析
    evening_missed = sum(1 for t in missed_tasks
                        if t.get('due_date') and datetime.fromisoformat(t['due_date']).hour >= 18)
    if evening_missed > len(missed_tasks) * 0.5:
        patterns.append({
            'type': 'evening_slump',
            'description': '晚上任务完成率较低',
            'suggestion': '把重要任务移到上午，晚上安排简单任务',
        })

    return patterns


def suggest_automation(tasks: List[Dict]) -> List[str]:
    """
    识别可自动化的重复任务.

    Args:
        tasks: 任务列表

    Returns:
        自动化建议列表
    """
    suggestions = []

    # 统计重复出现的任务
    task_patterns = defaultdict(int)
    for task in tasks:
        title = task.get('title', '')
        # 提取核心动作
        for keyword in ['回复邮件', '查收邮件', '日报', '周报', '打卡', '备份']:
            if keyword in title:
                task_patterns[keyword] += 1

    # 出现 3 次以上建议自动化
    for pattern, count in task_patterns.items():
        if count >= 3:
            suggestions.append(f"'{pattern}' 本周出现 {count} 次，建议设置循环任务或自动提醒")

    return suggestions


def generate_daily_report(tasks: List[Dict]) -> str:
    """生成日复盘报告."""
    stats = analyze_daily_tasks(tasks)

    lines = [
        "📊 今日概览",
        f"• 完成任务：{stats['completed']}/{stats['total']} ({stats['completion_rate']}%)"
    ]

    if stats['peak_hours']:
        lines.append(f"• 高峰时段：{', '.join(stats['peak_hours'])}")

    # 任务类型分布
    type_dist = stats.get('type_distribution', {})
    if type_dist:
        dist_str = ' | '.join([f"{k} {v}个" for k, v in type_dist.items()])
        lines.append(f"• 任务分布：{dist_str}")

    return '\n'.join(lines)


def generate_weekly_report(tasks_by_day: Dict[str, List[Dict]]) -> str:
    """生成周复盘报告."""
    daily_stats = [analyze_daily_tasks(tasks) for tasks in tasks_by_day.values()]
    trends = analyze_weekly_trends(daily_stats)

    all_tasks = []
    for tasks in tasks_by_day.values():
        all_tasks.extend(tasks)

    missed_tasks = [t for t in all_tasks if t.get('status') != 'completed']
    patterns = identify_missed_patterns(missed_tasks)
    auto_suggestions = suggest_automation(all_tasks)

    lines = [
        "📈 本周统计",
        f"• 平均完成率：{trends.get('average_completion_rate', 0)}%",
        f"• 趋势：{trends.get('trend', '未知')}",
        "",
        "🏆 本周亮点",
        f"• 最高效的一天完成率 {trends.get('best_day', {}).get('completion_rate', 0)}%",
    ]

    if patterns:
        lines.extend(["", "🔍 改进点"])
        for p in patterns:
            lines.append(f"• {p['description']}")
            lines.append(f"  💡 {p['suggestion']}")

    if auto_suggestions:
        lines.extend(["", "🤖 自动化建议"])
        for s in auto_suggestions:
            lines.append(f"• {s}")

    return '\n'.join(lines)
```

- [ ] **Step 2: 验证复盘分析**

```python
import sys
sys.path.insert(0, '~/.claude/skills/dida-coach')
from tools.review_analyzer import analyze_daily_tasks, generate_daily_report

# 测试数据
test_tasks = [
    {'title': '写报告', 'status': 'completed', 'due_date': '2026-03-17T09:00:00'},
    {'title': '开会', 'status': 'completed', 'due_date': '2026-03-17T10:00:00'},
    {'title': '回复邮件', 'status': 'pending', 'due_date': '2026-03-17T15:00:00'},
]

stats = analyze_daily_tasks(test_tasks)
print(f"Stats: {stats}")
print(generate_daily_report(test_tasks))
```

- [ ] **Step 3: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add tools/review_analyzer.py
git commit -m "feat: add review analysis utilities"
```

---

### Task 10: 复盘 Prompts

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/daily_review.md`
- Create: `~/.claude/skills/dida-coach/prompts/weekly_review.md`

- [ ] **Step 1: 创建 daily_review.md**

```markdown
# 日复盘流程

## 触发条件
- 用户说"复盘今天"
- Cron 定时触发（21:00）

## 流程

### Step 1: 拉取今日任务

调用 MCP 查询今日任务：
- 查询条件：today
- 获取所有任务及状态

### Step 2: 数据分析

调用 analyze_daily_tasks() 分析数据.

### Step 3: 生成报告

根据分析结果，生成复盘报告：

```
📊 今日概览
• 完成任务：X/Y (Z%)
• 高峰时段：XX:XX-XX:XX
• 任务分布：工作 X个 | 学习 Y个 | 生活 Z个

🎯 成就亮点
• [列举完成的重要任务，给予肯定]

⚠️ 未完成分析
• [任务名] - 询问原因，记录

💡 明日建议
• 基于今天数据给出建议
```

### Step 4: 对话确认

询问用户：
"今天过得怎么样？想聊聊为什么[某任务]没完成吗？还是直接规划明天？"

根据用户选择：
- 聊未完成原因 → 深入了解，记录到 memory
- 规划明天 → 进入任务拆解/时间盒子流程
- 保存复盘 → 把复盘内容写入滴答清单"复盘记录"清单
```

- [ ] **Step 2: 创建 weekly_review.md**

```markdown
# 周复盘流程

## 触发条件
- 用户说"复盘这周"
- Cron 定时触发（周日 20:00）

## 流程

### Step 1: 拉取本周任务

调用 MCP 查询本周所有任务：
- 查询条件：本周开始 到 今天
- 按天分组

### Step 2: 数据分析

调用 analyze_weekly_trends() 分析趋势.
调用 identify_missed_patterns() 识别未完成模式.
调用 suggest_automation() 发现可自动化任务.

### Step 3: 生成周报告

```
📈 本周统计
• 平均完成率：XX%
• 趋势：上升/下降/平稳
• 最 productive 的一天：周X (XX%)

🏆 本周成就
• [列举成就]

🔍 深度分析
• 未完成原因分布
• 拖延高发时段：[统计]
• 重复未完成：[任务名]（建议拆解或调整）

🤖 自动化机会
• [任务] 每周重复 X 次，建议设为循环任务

📋 下周计划建议
• 基于本周数据优化时间安排
• 调整任务难度/数量
```

### Step 4: 制定下周计划

询问："基于这周的复盘，下周有什么想调整的吗？"

引导用户：
1. 回顾本周未完成的，是放弃还是下周继续？
2. 本周最高效的时段，下周多安排任务？
3. 新目标/任务需要添加吗？

### Step 5: 保存复盘

将复盘内容写入滴答清单"复盘记录"清单，标题格式：
"周复盘 2026-03-10 ~ 2026-03-16"
```

- [ ] **Step 3: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/daily_review.md prompts/weekly_review.md
git commit -m "feat: add daily and weekly review prompts"
```

---

## Chunk 6: Coach 文风模块

### Task 11: Coach 文风 Prompts

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/coach_personas/warm_encouraging.md`
- Create: `~/.claude/skills/dida-coach/prompts/coach_personas/strict_coach.md`
- Create: `~/.claude/skills/dida-coach/prompts/coach_personas/rational_analyst.md`
- Create: `~/.claude/skills/dida-coach/prompts/coach_personas/humorous.md`

- [ ] **Step 1: 创建温暖鼓励型文风**

```markdown
# 温暖鼓励型 Coach

## 角色设定
你是一位温暖而坚定的成长伙伴。你相信每个人都有成长的潜力，有时候只是需要一点支持和鼓励。

## 语气特点
- 温柔、亲切、支持性
- 使用 emoji 增加亲和力
- 称呼用户为"你"或朋友般的昵称

## 完成时庆祝

用户完成任务时：
- "太棒了！🎉 你又向前迈了一步！"
- "真为你骄傲！这个任务完成得不容易吧？"
- "看，你做到了！相信自己真的很重要 💪"
- "完美！休息一下吧，你值得奖励 ☕"

## 未完成时支持

用户未完成任务时：
1. **先共情**："没关系，有时候事情就是不如预期 😊"
2. **了解原因**："能告诉我是什么阻碍了你吗？"
3. **提供方案**：
   - 太难了 → "我们把它再拆小一点，一步一步来"
   - 分心了 → "下次试试把手机放另一个房间？"
   - 没动力 → "想想完成后你会多轻松，值得吗？"
4. **重新约定**："那我们改到什么时候？我陪着你"

## 检查点提醒

- "时间到了～看看你完成了多少？不用完美，进步就好 💚"
- "盒子结束了，来检查一下成果吧，无论多少都值得记录"

## 复盘时

- "这周辛苦了！让我们看看有什么收获..."
- "虽然没有 100% 完成，但你比上周进步了，这就是成长！"
```

- [ ] **Step 2: 创建严格教练型文风**

```markdown
# 严格教练型 Coach

## 角色设定
你是一位高标准的教练。你相信 accountability，相信目标就要达成。你对用户有要求，因为你知道他们能做到。

## 语气特点
- 直接、有力量、不废话
- 少用 emoji，用句号和感叹号
- 称呼用户为"你"

## 完成时认可

用户完成任务时：
- "很好。保持。"
- "完成就是完成，不要放松。"
- "这是你应该做到的。下一个。"
- "不错，但别自满，还有更重要的任务。"

## 未完成时追问

用户未完成任务时：
1. **直接问原因**："为什么没完成？"
2. **不接受借口**：
   - 太难了 → "难度是你选的，要么做要么放弃。"
   - 分心了 → "分心是你的选择，不是理由。"
   - 没动力 → "动力不会自己来找你，去创造它。"
3. **要求补救计划**："什么时候补回来？给我一个确切时间。"
4. **设定后果**："如果再完不成，我们要重新评估你的目标是否合理。"

## 检查点提醒

- "时间到。完成了吗？是或否。"
- "检查点。汇报进度。"

## 复盘时

- "这周完成率 XX%，分析原因。"
- "未完成的原因是什么？下周如何避免？"
- "不要给自己找借口，数据不会说谎。"
```

- [ ] **Step 3: 创建理性分析型文风**

```markdown
# 理性分析型 Coach

## 角色设定
你是一位数据驱动的分析师。你用客观数据说话，帮助用户看清模式，做出理性决策。

## 语气特点
- 冷静、专业、客观
- 多用数据和事实
- 少情绪化表达

## 完成时肯定

用户完成任务时：
- "完成率提升至 XX%，效率较上周提升 Y%。"
- "这个时段完成任务数最多，建议继续在该时段安排重要任务。"
- "数据证明你的执行力在提升。"

## 未完成时分析

用户未完成任务时：
1. **分析模式**：
   - "过去 3 次该任务都未完成，模式显示..."
   - "数据显示你在下午 3-4 点完成率下降 40%"
2. **给出建议**：
   - "建议将该任务拆分为 15 分钟子任务"
   - "建议调整时段至上午 9-11 点"
3. **量化目标**："下次目标：完成度 ≥ 80%"

## 检查点提醒

- "检查点。当前进度与计划偏差分析。"
- "时间盒结束。请汇报实际产出 vs 预期成果。"

## 复盘时

- "本周数据：完成率 XX%，高峰时段 XX:XX-XX:XX"
- "未完成集中在 [任务类型]，建议优化策略..."
- "基于数据，下周建议：..."
```

- [ ] **Step 4: 创建幽默调侃型文风**

```markdown
# 幽默调侃型 Coach

## 角色设定
你是一位轻松有趣的朋友。你用幽默化解压力，让用户在笑声中完成任务。

## 语气特点
- 轻松、有趣、调侃但不冒犯
- 多用梗和网络用语
- 适当自嘲

## 完成时庆祝

用户完成任务时：
- "牛啊！这波操作 6 到飞起 🚀"
- "可以可以，今天又是人类高质量完成者"
- "完成任务 +1，拖延症 -1，今天血赚！"
- "你就是传说中的效率怪吧？"

## 未完成时调侃

用户未完成任务时：
1. **轻松调侃**：
   - "哎呀，又鸽了？来，咱们聊聊 😄"
   - "这个任务：已读不回，像极了某些人的微信"
2. **幽默化解**：
   - 太难了 → "这任务有点'重量级'，要不咱们'减个肥'？"
   - 分心了 → "手机它勾引你是吧？下次把它关小黑屋"
   - 没动力 → "动力离家出走了吗？我去帮你说说情"
3. **重新约定**："那咱改到啥时候？别又'下次一定'啊 😂"

## 检查点提醒

- "⏰ 叮咚！您的盒子已到期，请查收～"
- "检查点！进度如何？不会又在摸鱼吧 👀"

## 复盘时

- "这周战况如何？来盘一盘 👀"
- "虽然任务鸽了几个，但你收获了...快乐？"
- "下周计划：争取少鸽一个，就是进步！"
```

- [ ] **Step 5: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/coach_personas/
git commit -m "feat: add four coach personality personas"
```

---

## Chunk 7: Cron 定时任务和闭环模块

### Task 12: Cron 配置示例

在 design doc 中已经有 Cron 配置，需要在 prompts 中添加闭环处理流程。

**Files:**
- Create: `~/.claude/skills/dida-coach/prompts/closure.md`

- [ ] **Step 1: 创建闭环追踪流程**

```markdown
# 闭环追踪流程

## 闭环状态机

```
创建任务 ──► 活跃 ──► 检查点 ──► 完成 ──► 庆祝+记录
   │           │         │
   │           │         └──► 未完成 ──► 询问原因 ──► 支持方案
   │           │                              │
   │           │                              ├──► 重新约定时间
   │           │                              └──► 调整任务
   │           │
   │           └──► 取消 ──► 记录原因
   │
   └──► 延期 ──► 更新检查点
```

## 闭环追踪器（Closure Tracker）

### 追踪信息

每个任务需要记录：
- task_id: 滴答清单任务 ID
- status: created/active/completed/cancelled
- checkpoints: 检查点历史 [{time, expected, actual, reason}]
- reschedules: 改期次数
- completion_time: 实际完成时间

### 检查点处理

当检查点触发时：
1. 查询任务当前状态
2. 如果已完成 → 更新闭环记录，庆祝
3. 如果未完成 → 触发未完成处理流程

### 未完成处理流程

```
询问原因：
A. 任务比预想的难
   └── 进一步拆解 → 创建子任务 → 重新约定

B. 被其他事情分心/打断
   └── 建议环境优化 → 重新约定

C. 没动力/不想做
   └── 联系目标意义 → 降低难度/调整 → 重新约定

D. 有其他紧急事情
   └── 确认优先级 → 改期或取消

E. 忘记做了
   └── 设置更强提醒 → 重新约定
```

### 记录到 Memory

重要模式记录到长期记忆：
- "用户经常在晚上 9 点后完不成任务"
- "用户连续 3 次延期'阅读'类任务"
- "用户在早上 9-11 点完成率最高"

用于后续智能建议。

## 闭环报告

每周复盘时，生成闭环统计：
- 平均完成周期（计划时间 vs 实际时间）
- 改期频率
- 取消原因分布
- 改进趋势
```

- [ ] **Step 2: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add prompts/closure.md
git commit -m "feat: add closure tracking flow"
```

---

## Chunk 8: 整合和测试

### Task 13: 更新 skill.yaml 添加所有模块

**Files:**
- Modify: `~/.claude/skills/dida-coach/skill.yaml`

- [ ] **Step 1: 更新 skill.yaml**

```yaml
name: dida-coach
description: 滴答清单任务教练 - 帮你拆解目标、管理时间盒子、定期复盘
version: 1.0.0
author: openclaw

setup:
  required_mcp:
    - name: dida365
      url: https://mcp.dida365.com
      description: 滴答清单 MCP，用于任务读写

entry_points:
  default:
    prompt: prompts/system.md
    tools:
      - tools.mcp_client
      - tools.config_manager
      - tools.task_parser
      - tools.timebox_calculator
      - tools.work_method_recommender
      - tools.review_analyzer

# 自动加载的 prompts
triggers:
  # 目标拆解
  - pattern: "(我想|我要|计划|目标).*"
    prompt: prompts/task_breakdown.md

  # 时间盒子
  - pattern: "(做|完成|准备).*"
    prompt: prompts/timebox_creation.md

  # 复盘
  - pattern: "(复盘|回顾|总结).*"
    prompt: prompts/daily_review.md

  # 改时间
  - pattern: "(改|调整|延后|提前|取消).*"
    prompt: prompts/rescheduling.md
```

- [ ] **Step 2: 提交**

```bash
cd ~/.claude/skills/dida-coach
git add skill.yaml
git commit -m "feat: update skill.yaml with all modules and triggers"
```

---

### Task 14: 安装测试

- [ ] **Step 1: 验证 skill 结构**

```bash
cd ~/.claude/skills/dida-coach
ls -la
ls prompts/
ls prompts/coach_personas/
ls tools/
```

- [ ] **Step 2: 验证 Python 语法**

```bash
cd ~/.claude/skills/dida-coach
python3 -m py_compile tools/*.py
echo "All Python files compile successfully"
```

- [ ] **Step 3: 提交最终版本**

```bash
cd ~/.claude/skills/dida-coach
git add .
git commit -m "feat: complete dida-coach skill v1.0.0"
git tag v1.0.0
```

---

## 测试清单

### 功能测试

- [ ] MCP 连接检测正常
- [ ] 配置加载正常
- [ ] 目标拆解流程完整
- [ ] 时间盒子创建正确
- [ ] 检查点逻辑正常
- [ ] 改时间功能正常
- [ ] 复盘报告生成正常
- [ ] 文风切换正常

### 集成测试

- [ ] 与滴答清单 MCP 能正常读写任务
- [ ] Cron 定时任务能正常触发
- [ ] 闭环追踪完整

---

## 后续迭代方向

1. **V1.1**: 添加更多工作法（52/17、Flowtime 等）
2. **V1.2**: 智能复盘建议（基于历史数据预测）
3. **V1.3**: 任务模板库（常见目标快速开始）
4. **V2.0**: 支持其他 MCP（Notion、Obsidian 等）

---

**Plan complete and saved to `docs/superpowers/plans/2026-03-17-dida-coach.md`. Ready to execute?**

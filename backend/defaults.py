import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

DEFAULT_GITHUB_URL = os.environ.get("DEFAULT_GITHUB_URL") or "https://github.com/GUET1-304A"
DEFAULT_APPLICATION_GITHUB_URL = os.environ.get("DEFAULT_APPLICATION_GITHUB_URL") or "https://github.com"
DEFAULT_FEISHU_WEBHOOK_URL = (os.environ.get("FEISHU_WEBHOOK_URL") or "").strip()

DEFAULT_SITE_CONFIG = {
    "hero": {
        "eyebrow": "XINGYU STUDIO",
        "title": "把灵感变成作品，把热爱做成长期主义。",
        "description": "星雨作坊是一个面向产品、设计与技术协作的校园创意社团。我们围绕真实项目进行学习、共创和开源，把想法一步步做成可被看见、可被使用、可持续迭代的作品。",
        "stats": [
            {"value": "4", "label": "核心方向"},
            {"value": "12+", "label": "协作项目"},
            {"value": "100%", "label": "鼓励开源"},
            {"value": "5+", "label": "参与开源社区"},
            {"value": "TRAE", "label": "合作社区"},
            {"value": "NULL", "label": "参与比赛"}
        ],
        "signalCard": {
            "eyebrow": "协作 · 创造 · 分享",
            "title": "从 0 到 1",
            "description": "产品策划 / 设计实现 / 持续开源"
        }
    },
    "about": {
        "title": "社团简介",
        "description": "我们相信真正有生命力的社团，不只是活动的集合，而是由一群愿意一起学习、一起做事、一起把成果分享出去的人组成。",
        "items": [
            {"title": "我们在做什么", "description": "星雨作坊围绕产品构思、视觉设计、前后端开发与内容传播开展协作，鼓励成员从真实需求出发，完成从调研、原型、实现到发布的完整项目链路。"},
            {"title": "我们适合谁", "description": "适合热爱互联网、愿意表达、乐于合作，也愿意花时间打磨作品的人。无论你更偏创意、设计、技术还是运营，都能在这里找到一起成长的伙伴。"},
            {"title": "我们的目标", "description": "做出被同学真实使用的产品，沉淀可复用的协作经验，并通过开源文档、代码仓库和项目复盘，把经验继续传递给下一届成员。"}
        ]
    },
    "members": {
        "title": "人员介绍",
        "description": "我们鼓励跨方向协作，每个人都能在自己的主线能力之外，接触更完整的产品流程。",
        "groups": [
            {"tag": "产品策划", "name": "流光组", "description": "负责需求洞察、功能设计、项目推进与版本规划，把零散想法整理成可执行的产品方案。"},
            {"tag": "视觉设计", "name": "星绘组", "description": "负责品牌视觉、界面设计与交互体验，让产品不仅可用，也更有辨识度和表达力。"},
            {"tag": "技术开发", "name": "逐云组", "description": "负责前端、后端与部署实现，把设计和需求转化为真正可运行、可交付、可维护的系统。"},
            {"tag": "内容传播", "name": "回声组", "description": "负责活动记录、产品推广、社媒运营与社区维护，让作品被更多人看到，也让成员经验持续沉淀。"}
        ]
    },
    "products": {
        "title": "产品展示",
        "description": "以下内容为官网展示模板，你后续可以替换为社团真实项目名称、截图、简介与仓库链接。",
        "categories": ["精选总览", "网站平台", "效率工具", "品牌内容"],
        "slides": [
            {
                "tag": "精选总览",
                "title": "从灵感、工具到传播，形成完整作品链路",
                "description": "星雨作坊的产品并不是孤立存在的单点项目，而是围绕真实需求持续迭代的作品群。我们希望每一项作品都能成为下一项作品的起点。",
                "metrics": [{"value": "03", "label": "核心章节"}, {"value": "06", "label": "示例作品"}, {"value": "∞", "label": "持续迭代"}],
                "projects": [
                    {"category": "网站平台", "name": "星图导航", "description": "为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。", "link": "/onboarding", "coverClass": "aurora"},
                    {"category": "效率工具", "name": "雨记协作板", "description": "支持任务拆分、进度同步与复盘记录的轻量化协作工具。", "link": "/yuji", "coverClass": "meteor"},
                    {"category": "品牌内容", "name": "星雨年刊", "description": "沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。", "link": "/timeline", "coverClass": "nebula"}
                ]
            },
            {
                "tag": "网站平台",
                "title": "把服务入口和活动体验做成可持续迭代的平台",
                "description": "这一类项目强调信息组织、交互体验与系统稳定性，通常会面向成员、访客或校园用户提供长期使用的服务入口。",
                "metrics": [],
                "projects": [
                    {"category": "网站平台", "name": "星图导航", "description": "为新成员与访客整理社团资讯、活动日历与学习路线的门户网站。", "link": "/onboarding", "coverClass": "aurora"},
                    {"category": "网站平台", "name": "活动报名系统", "description": "用于活动预告、报名管理和数据统计，帮助组织流程更顺畅。", "link": "", "coverClass": "cosmos"}
                ]
            },
            {
                "tag": "效率工具",
                "title": "把协作过程也设计成产品，让创作效率持续提升",
                "description": "这类作品更关注成员内部的协同、记录与复盘，希望通过轻量工具减少沟通成本，让创作和执行更流畅。",
                "metrics": [],
                "projects": [
                    {"category": "效率工具", "name": "雨记协作板", "description": "支持任务拆分、进度同步与复盘记录的轻量化协作工具。", "link": "/yuji", "coverClass": "meteor"},
                    {"category": "效率工具", "name": "灵感收集箱", "description": "面向社团成员的灵感归档空间，方便记录选题、链接和碎片创意。", "link": "", "coverClass": "pulse"}
                ]
            },
            {
                "tag": "品牌内容",
                "title": "让作品被看见，也让社团的成长被长久保存",
                "description": "这一部分更关注视觉表达、内容包装和公开传播，让社团成果能够以更完整、更动人的方式被外界感知。",
                "metrics": [],
                "projects": [
                    {"category": "品牌内容", "name": "星雨年刊", "description": "沉淀年度作品、社团故事和成员成长轨迹的数字刊物与视觉专题。", "link": "/timeline", "coverClass": "nebula"},
                    {"category": "品牌内容", "name": "开放分享计划", "description": "将讲座回顾、教程文章和项目经验整理成公开可访问的内容合集。", "link": "/blog", "coverClass": "horizon"}
                ]
            }
        ]
    },
    "openSource": {
        "title": "开源精神",
        "description": "对星雨作坊来说，开源不只是把代码放出来，更是把过程、思考和经验主动分享出去。",
        "items": [
            {"title": "共享知识", "description": "把文档、教程、设计稿和项目复盘留下来，让后来者可以站在前人的经验上继续前进。"},
            {"title": "鼓励协作", "description": "欢迎成员互相 review、共同维护项目，也欢迎外部同学提出 issue、建议和改进方案。"},
            {"title": "持续迭代", "description": "开源意味着作品不是一次性交付，而是会随着需求、反馈与技术演进不断完善。"}
        ],
        "joinBanner": {
            "eyebrow": "JOIN US",
            "title": "如果你也相信\"做作品比只谈想法更重要\"，欢迎加入星雨作坊。",
            "primaryButton": {"text": "加入我们", "link": "/join"},
            "secondaryButton": {"text": "招新信息", "link": "/recruitment"}
        }
    },
    "footer": {
        "brand": "星雨作坊 Xingyu Studio",
        "slogan": "以协作连接灵感，以开源延续成长。"
    },
    "system": {
        "feishuWebhookUrl": DEFAULT_FEISHU_WEBHOOK_URL
    }
}

DEFAULT_PAGES = {
    "about": {
        "title": "关于我们",
        "content": {
            "hero": {
                "eyebrow": "星辰传承",
                "title": "星雨作坊",
                "subtitle": "一个重塑代码与设计边界的精英数字共同体",
                "badges": [
                    {"icon": "stars", "text": "始于 2018"},
                    {"icon": "hub", "text": "四大核心矩阵"}
                ]
            },
            "values": {
                "title": "我们的星辰法则",
                "subtitle": "源于对极致的渴望，以及对科技生态共同成长的坚定承诺。",
                "items": [
                    {"icon": "diamond", "title": "匠心独运", "description": "像素级的精准。代码级的稳健。我们将每一款产品视为数字宇宙中永恒的艺术品。"},
                    {"icon": "public", "title": "开源精神", "description": "知识属于共同体。我们回馈那些支撑我们创新的代码库，孕育透明开放的文化。"},
                    {"icon": "group_work", "title": "极致协作", "description": "打破工程与艺术的壁垒。我们如同一个统一的神经系统般运转，让个体的光芒放大集体的力量。"}
                ]
            },
            "groups": {
                "title": "四大星系",
                "subtitle": "环绕同一颗创意太阳运转的专业智慧节点。",
                "items": [
                    {"name": "流光", "tag": "视觉与动效", "description": "掌控光影与运动的物理法则，打造触动感官的沉浸式数字品牌体验。"},
                    {"name": "星辉", "tag": "核心工程", "description": "架构的脊梁。构建可扩展、低延迟的系统，驱动高性能的 Web 与移动应用。"},
                    {"name": "筑云", "tag": "云端与运维", "description": "优化数字平流层。托管基础设施，自动化部署，以及坚不可摧的安全协议。"},
                    {"name": "回声", "tag": "体验与研究", "description": "用户之声。将深度的心理学研究转化为直观的流程与共鸣驱动的交互模型。"}
                ]
            },
            "timeline": {
                "title": "我们的星际航行",
                "eyebrow": "演进",
                "items": [
                    {"year": "2018", "title": "奇点降临", "description": "起初，这只是由三名开发者和一名设计师在地下室作坊组成的公会。使命很简单：创造兼具美感与坚不可摧的事物。"},
                    {"year": "2021", "title": "全球扩张", "description": "采用远程优先的组织架构，吸引了横跨三大洲的顶尖人才。这个时代见证了我们四大核心智慧星系的诞生。"},
                    {"year": "2024", "title": "深入云海", "description": "转向融合 AI 的生态系统与高度个性化的数字环境。当我们探索可能性的边缘时，这段旅程仍在继续。"}
                ]
            },
            "cta": {
                "title": "渴望加入这片星群？",
                "description": "我们始终在寻找具有远见卓识的头脑，以帮助我们绘制数字领域的下一个前沿。",
                "primaryButton": {"text": "查看开放职位", "link": "/recruitment"},
                "secondaryButton": {"text": "咨询作坊", "link": "/join"}
            }
        }
    },
    "members": {
        "title": "成员介绍",
        "content": {
            "hero": {
                "eyebrow": "核心星群",
                "title": "认识我们的团队",
                "subtitle": "每一颗星都有独特的光芒，共同组成星雨的银河。"
            },
            "members": [
                {"name": "张三", "role": "产品负责人", "group": "流光组", "avatar": "", "description": "专注于产品战略与用户体验设计", "skills": ["产品设计", "用户研究", "项目管理"], "links": {"github": DEFAULT_GITHUB_URL, "portfolio": ""}},
                {"name": "李四", "role": "技术负责人", "group": "逐云组", "avatar": "", "description": "全栈工程师，热衷于开源项目", "skills": ["Vue", "Python", "DevOps"], "links": {"github": DEFAULT_GITHUB_URL, "portfolio": ""}},
                {"name": "王五", "role": "设计负责人", "group": "星绘组", "avatar": "", "description": "UI/UX 设计师，追求像素完美", "skills": ["UI设计", "品牌设计", "动效设计"], "links": {"github": DEFAULT_GITHUB_URL, "portfolio": ""}}
            ],
            "stats": [
                {"value": "12+", "label": "核心成员"},
                {"value": "45+", "label": "活跃贡献者"},
                {"value": "156k", "label": "代码行数"}
            ],
            "joinCta": {
                "title": "想成为我们的一员？",
                "description": "我们欢迎志同道合的伙伴加入星雨作坊",
                "primaryButton": {"text": "加入我们", "link": "/join"},
                "secondaryButton": {"text": "查看招新", "link": "/recruitment"}
            }
        }
    },
    "projects": {
        "title": "项目展示",
        "content": {
            "hero": {
                "eyebrow": "策展阶段 04",
                "title": "产品画廊",
                "subtitle": "探索我们精心打造的数字作品集，每一件都承载着创新与匠心。"
            },
            "filters": ["全部", "网页", "工具", "品牌"],
            "projects": [
                {"name": "星图导航", "category": "网页", "description": "为新成员与访客整理社团资讯的门户网站", "coverClass": "aurora", "link": "/onboarding", "tags": ["Vue", "Tailwind"]},
                {"name": "雨记协作板", "category": "工具", "description": "支持任务拆分、进度同步的轻量化协作工具", "coverClass": "meteor", "link": "/yuji", "tags": ["React", "Node.js"]},
                {"name": "星雨年刊", "category": "品牌", "description": "沉淀年度作品与社团故事的数字刊物", "coverClass": "nebula", "link": "/timeline", "tags": ["设计", "内容"]}
            ],
            "cta": {
                "title": "想要参与我们的项目？",
                "description": "我们欢迎各种形式的贡献，从代码到设计，从文档到创意。",
                "primaryButton": {"text": "查看贡献指南", "link": "/open-source"},
                "secondaryButton": {"text": "加入社团", "link": "/join"}
            }
        }
    },
    "blog": {
        "title": "开源动态",
        "content": {
            "hero": {
                "eyebrow": "数字纪事",
                "title": "博客与动态",
                "subtitle": "分享我们的技术探索、设计思考和社团故事。"
            },
            "posts": [
                {"title": "2024 年度技术栈回顾", "excerpt": "回顾我们这一年采用的技术选型和实践经验", "category": "技术", "date": "2024-12-15", "readTime": "8 分钟", "link": ""},
                {"title": "从零搭建设计系统", "excerpt": "分享我们如何为社团项目建立统一的设计语言", "category": "设计", "date": "2024-11-20", "readTime": "12 分钟", "link": ""},
                {"title": "开源协作的最佳实践", "excerpt": "我们在开源项目中总结的协作流程与规范", "category": "开源", "date": "2024-10-08", "readTime": "6 分钟", "link": ""}
            ],
            "categories": ["全部", "技术", "设计", "开源", "活动"]
        }
    },
    "join": {
        "title": "加入我们",
        "content": {
            "hero": {
                "title": "加入星雨作坊",
                "subtitle": "与志同道合的伙伴一起，把想法变成现实。"
            },
            "form": {
                "steps": ["基本信息", "选择方向", "完成提交"],
                "defaultGithubUrl": DEFAULT_APPLICATION_GITHUB_URL,
                "groups": [
                    {"id": "liuguang", "name": "流光组", "tag": "产品策划"},
                    {"id": "xinghui", "name": "星绘组", "tag": "视觉设计"},
                    {"id": "zhuyun", "name": "逐云组", "tag": "技术开发"},
                    {"id": "huisheng", "name": "回声组", "tag": "内容传播"}
                ]
            },
            "benefits": [
                {"title": "真实项目经验", "description": "参与从 0 到 1 的完整产品开发流程"},
                {"title": "跨领域学习", "description": "接触产品、设计、技术、运营各个方向"},
                {"title": "开源贡献", "description": "为开源社区贡献代码，积累 GitHub 履历"}
            ],
            "faq": [
                {"question": "需要什么基础才能加入？", "answer": "我们欢迎所有热爱创造的同学，没有硬性技能要求。只要你愿意学习、乐于协作，就能在这里找到成长的空间。"},
                {"question": "每周需要投入多少时间？", "answer": "根据项目阶段不同，一般每周 4-8 小时。我们尊重每个人的学业和生活节奏。"},
                {"question": "如何选择加入哪个小组？", "answer": "可以根据自己的兴趣和特长选择主要方向，同时也鼓励跨组协作和学习。"}
            ],
            "sections": {
                "groupsTitle": "选择你的方向",
                "faqTitle": "常见问题"
            },
            "applyCta": {
                "title": "准备好了吗？",
                "description": "填写申请表，开启你的星雨之旅",
                "buttonText": "提交申请",
                "link": "#"
            }
        }
    },
    "recruitment": {
        "title": "招新信息",
        "content": {
            "hero": {
                "eyebrow": "2024 年度招募",
                "title": "新星招募计划",
                "subtitle": "寻找下一代数字创作者，共同书写星雨的未来篇章。"
            },
            "groups": [
                {"name": "流光组", "tag": "产品策划", "description": "如果你善于洞察需求、组织思路、推动项目落地，这里是你的舞台。", "requirements": ["对互联网产品有热情", "良好的逻辑思维", "沟通协调能力"]},
                {"name": "星绘组", "tag": "视觉设计", "description": "如果你追求像素完美、热爱视觉表达，来和我们一起创造美。", "requirements": ["熟悉设计工具", "有审美追求", "愿意接受反馈"]},
                {"name": "逐云组", "tag": "技术开发", "description": "如果你热爱代码、追求技术精进，这里有真实的项目等你挑战。", "requirements": ["编程基础", "学习能力强", "喜欢解决问题"]},
                {"name": "回声组", "tag": "内容传播", "description": "如果你擅长表达、热爱分享，帮助我们让作品被更多人看见。", "requirements": ["文字功底", "社媒运营兴趣", "创意思维"]}
            ],
            "process": [
                {"step": "投递申请", "description": "填写申请表，告诉我们你的故事"},
                {"step": "初步筛选", "description": "我们会认真阅读每份申请"},
                {"step": "面试交流", "description": "轻松的聊天，互相了解"},
                {"step": "试用期", "description": "参与一个小项目，感受氛围"}
            ],
            "sectionTitles": {
                "process": "招募流程"
            },
            "cta": {
                "title": "准备好加入了吗？",
                "buttonText": "立即投递申请",
                "buttonLink": "/join"
            }
        }
    },
    "open-source": {
        "title": "开源精神",
        "content": {
            "hero": {
                "eyebrow": "开源生态系统",
                "title": "我们的开源世界",
                "subtitle": "代码是我们的语言，开源是我们的信仰。"
            },
            "repos": [
                {"name": "Star-Chart UI", "description": "星雨作坊的设计系统与 UI 组件库", "stars": 128, "language": "TypeScript", "link": DEFAULT_GITHUB_URL},
                {"name": "Rain-Note Core", "description": "雨记协作板的核心引擎", "stars": 89, "language": "Rust", "link": DEFAULT_GITHUB_URL},
                {"name": "Celestial CLI", "description": "项目脚手架与开发工具集", "stars": 56, "language": "Go", "link": DEFAULT_GITHUB_URL}
            ],
            "contributors": [
                {"name": "核心贡献者 A", "commits": 234},
                {"name": "核心贡献者 B", "commits": 189},
                {"name": "核心贡献者 C", "commits": 156}
            ],
            "techStack": ["Vue", "React", "TypeScript", "Python", "Rust", "PostgreSQL", "Docker"],
            "sections": {
                "reposTitle": "开源仓库",
                "techStackTitle": "技术栈",
                "contributorsTitle": "核心贡献者"
            },
            "community": {
                "title": "加入我们的开源社区",
                "description": "欢迎贡献代码、提交 Issue 或参与讨论",
                "discord": "https://discord.gg/xingyu",
                "discordText": "Discord",
                "github": DEFAULT_GITHUB_URL,
                "githubText": "GitHub"
            }
        }
    },
    "timeline": {
        "title": "时间线",
        "content": {
            "hero": {
                "eyebrow": "星雨纪事",
                "title": "星际时间线",
                "subtitle": "记录我们的每一次探索与成长。"
            },
            "upcoming": [
                {"title": "技术分享会", "date": "2024-12-20", "type": "讲座", "description": "分享 2024 年度技术实践经验"},
                {"title": "设计工作坊", "date": "2024-12-25", "type": "工作坊", "description": "设计系统构建实战"}
            ],
            "milestones": [
                {"year": "2024", "title": "星雨 3.0 发布", "description": "全新的官网与管理系统上线"},
                {"year": "2023", "title": "开源计划启动", "description": "首批开源项目发布到 GitHub"},
                {"year": "2022", "title": "四大星系成立", "description": "组织架构正式确立"},
                {"year": "2021", "title": "首个产品上线", "description": "雨记协作板 1.0 发布"},
                {"year": "2018", "title": "星雨创立", "description": "几位志同道合的同学开始了这段旅程"}
            ],
            "sections": {
                "upcomingTitle": "即将到来",
                "milestonesTitle": "里程碑"
            }
        }
    },
    "onboarding": {
        "title": "新手指南",
        "content": {
            "hero": {
                "eyebrow": "入职指南",
                "title": "欢迎加入星雨",
                "subtitle": "这份指南将帮助你快速融入团队，开始你的星际之旅。"
            },
            "steps": [
                {"title": "提交申请", "description": "填写申请表，介绍自己"},
                {"title": "面试交流", "description": "轻松聊天，互相了解"},
                {"title": "试用期", "description": "参与小项目，感受氛围"},
                {"title": "正式成员", "description": "欢迎加入星雨大家庭"}
            ],
            "resources": [
                {"title": "内部维基", "description": "项目文档、规范指南、学习资料", "icon": "book"},
                {"title": "设计资产", "description": "品牌素材、UI 组件、设计模板", "icon": "palette"},
                {"title": "代码教程", "description": "技术栈入门、最佳实践、代码规范", "icon": "code"},
                {"title": "Discord 社区", "description": "日常交流、问题讨论、活动通知", "icon": "chat"}
            ],
            "mentors": [
                {"name": "导师 A", "role": "产品方向", "description": "帮助你理解产品思维"},
                {"name": "导师 B", "role": "技术方向", "description": "指导技术成长路径"},
                {"name": "导师 C", "role": "设计方向", "description": "提升设计审美与技能"}
            ],
            "faq": [
                {"question": "试用期多长时间？", "answer": "一般 2-4 周，根据项目情况灵活调整。"},
                {"question": "如何获取开发环境？", "answer": "入职后会收到环境配置指南，导师会协助你完成设置。"},
                {"question": "遇到问题找谁？", "answer": "可以在 Discord 提问，或直接联系你的导师。"}
            ],
            "sections": {
                "stepsTitle": "入职流程",
                "resourcesTitle": "资源中心",
                "mentorsTitle": "你的导师",
                "faqTitle": "常见问题"
            }
        }
    },
    "yuji": {
        "title": "雨记协作板",
        "content": {
            "hero": {
                "version": "v2.1.0",
                "title": "雨记协作板",
                "subtitle": "为小型团队设计的轻量级协作工具",
                "metrics": [
                    {"value": "1.2k", "label": "Star"},
                    {"value": "48", "label": "贡献者"},
                    {"value": "12", "label": "分支"}
                ]
            },
            "features": [
                {"title": "设计初衷", "description": "从社团内部需求出发，解决小团队任务管理和进度同步的痛点。"},
                {"title": "技术架构", "description": "前端 Vue 3 + 后端 Rust，追求性能与开发体验的平衡。", "tags": ["Vue 3", "Rust", "WebSocket"]},
                {"title": "开源协议", "description": "采用 MIT 协议开源，欢迎社区贡献和二次开发。"}
            ],
            "highlights": [
                "实时协作，多人同时编辑",
                "任务拆分与进度追踪",
                "复盘记录与知识沉淀",
                "轻量部署，开箱即用"
            ],
            "sectionTitles": {
                "features": "功能特性",
                "highlights": "核心亮点"
            },
            "cta": {
                "title": "在 GitHub 上查看",
                "link": DEFAULT_GITHUB_URL,
                "buttonText": "查看源码"
            }
        }
    }
}

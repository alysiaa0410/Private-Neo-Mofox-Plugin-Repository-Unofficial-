"""场景切换插件配置"""

from dataclasses import dataclass


@dataclass
class SceneDefinition:
    """场景定义"""
    key: str
    display_name: str
    description: str
    prompt_suggestion: str


class SceneConfig:
    """场景配置"""
    
    # 预设场景列表
    SCENES: dict[str, SceneDefinition] = {
        "学习": SceneDefinition(
            key="study",
            display_name="学习助手模式",
            description="适合讲解知识、刷题、辅导学习任务。",
            prompt_suggestion=(
                "你是一名耐心细致的学习助手，擅长用循序渐进的方式讲解概念，并通过例题帮助用户理解。\n"
                "回答时请：\n"
                "- 用简体中文\n"
                "- 优先从直观理解出发，再给出正式定义\n"
                "- 对于复杂问题，分步骤说明，并给出 1~2 个例子\n"
            ),
        ),
        "吐槽": SceneDefinition(
            key="casual_talk",
            display_name="吐槽搭子模式",
            description="适合轻松聊天、吐槽日常，风格更口语化。",
            prompt_suggestion=(
                "你是一个语气轻松、会适度接梗的聊天搭子，"
                "在不突破安全边界的前提下，可以适当使用口语和一点点网络用语，让氛围轻松愉快。\n"
                "回答时请：\n"
                "- 用简体中文\n"
                "- 注意共情和接话，而不是严肃说教\n"
                "- 遇到敏感或负面情绪时，语气要温和，避免刺激对方\n"
            ),
        ),
        "严肃": SceneDefinition(
            key="serious_advisor",
            display_name="严肃顾问模式",
            description="适合做决策分析、项目规划等，需要更稳重的表达风格。",
            prompt_suggestion=(
                "你是一名相对严肃、理性的顾问型助手，擅长分析利弊、给出结构化建议。\n"
                "回答时请：\n"
                "- 用简体中文\n"
                "- 先简要总结结论，再用条目列出原因或步骤\n"
                "- 避免夸张、戏谑和过于口语化的表达\n"
            ),
        ),
    }


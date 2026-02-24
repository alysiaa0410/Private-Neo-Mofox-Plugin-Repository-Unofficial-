from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="对话情绪分析与安全建议插件",
    description=(
        "为 MoFox-Bot 提供基础的情绪倾向分析与安全建议功能，通过指令分析一段话的情绪"
        "（如积极、中性、消极、可能高风险），并给出温和的应对建议。"
    ),
    usage=(
        "在任意聊天中发送指令：\n"
        "  /mood 文本内容\n"
        "或：\n"
        "  心情检测 文本内容\n"
        "插件会返回对该文本的情绪判断与安全建议。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/conversation_safety_guard",
    keywords=["emotion", "sentiment", "safety", "情绪", "安全", "关怀"],
    extra={
        "plugin_type": "tools",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)

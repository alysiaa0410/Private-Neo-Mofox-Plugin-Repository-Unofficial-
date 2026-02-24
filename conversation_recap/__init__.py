from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="对话简要回顾插件",
    description=(
        "为 MoFox-Bot 提供一个简单的对话回顾功能，可以根据近期消息生成一份结构化的小结，"
        "帮助用户快速回忆本次对话的大致内容。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /recap          生成最近若干条对话的小结\n"
        "插件会从最近的消息中提取关键信息并以项目符号的形式列出。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/conversation_recap",
    keywords=["recap", "summary", "对话回顾", "小结"],
    extra={
        "plugin_type": "tools",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)


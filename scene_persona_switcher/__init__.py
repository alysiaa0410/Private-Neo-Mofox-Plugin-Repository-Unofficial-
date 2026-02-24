from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="多角色预设与场景切换插件",
    description=(
        "为 MoFox-Bot 提供多套可配置的人设与场景预设（如学习助手、日常聊天、严肃顾问等），"
        "通过指令一键切换当前会话使用的提示词与语气说明，增强可玩性与可控性。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /scene list         查看可用场景\n"
        "  /scene 学习         切换到“学习助手”人设\n"
        "  /scene 吐槽         切换到“吐槽搭子”人设\n"
        "切换后，插件会返回该场景推荐的人设说明与建议提示词，你可以将其整合到 KFC/AFC 配置中。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/scene_persona_switcher",
    keywords=["persona", "scene", "prompt", "人设", "场景切换", "提示词"],
    extra={
        "plugin_type": "prompt",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)


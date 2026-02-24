from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="亲密度与成就系统插件",
    description=(
        "为 MoFox-Bot 增加亲密度与成就系统，根据对话频率和时长逐步提升用户与机器人的亲密度，"
        "并在达到阈值时解锁成就称号，增强长期陪伴感和可玩性。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /affinity         查看当前亲密度与已解锁成就\n"
        "插件会根据本进程内记录的对话交互情况，给出一个简单的亲密度等级与称号。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/affinity_achievements",
    keywords=["affinity", "achievement", "gamification", "亲密度", "成就", "陪伴"],
    extra={
        "plugin_type": "personality",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)


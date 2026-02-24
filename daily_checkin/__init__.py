from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="每日签到与连击插件",
    description=(
        "为 MoFox-Bot 增加一个轻量的每日签到系统，记录用户当日是否签到，并给出连击天数和简单奖励提示，"
        "增强用户粘性和互动乐趣（数据仅在当前进程内有效）。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /checkin          今日签到\n"
        "  /checkin status   查看当前连击天数\n"
        "插件会在本进程内记录你的最后签到日期，并根据连续签到天数返回不同的提示。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/daily_checkin",
    keywords=["checkin", "sign", "gamification", "签到", "连击"],
    extra={
        "plugin_type": "entertainment",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)


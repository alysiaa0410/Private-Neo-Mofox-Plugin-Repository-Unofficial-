from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="轻量 FAQ 与知识库增强插件",
    description=(
        "为 MoFox-Bot 增加一个基于内置配置的轻量 FAQ/知识库系统，"
        "对常见问题给出稳定一致的标准答案，降低大模型调用成本并提升可控性。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /faq 关键字\n"
        "例如：/faq 帮助\n"
        "插件会尝试在内置 FAQ 条目中匹配最相关的问题并返回标准答案。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/simple_faq_knowledge",
    keywords=["faq", "knowledge", "文档", "帮助", "知识库"],
    extra={
        "plugin_type": "tools",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)

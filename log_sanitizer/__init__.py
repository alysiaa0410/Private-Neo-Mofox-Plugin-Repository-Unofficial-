from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="日志隐私脱敏插件",
    description=(
        "在调试与记录日志时，对可能包含手机号、邮箱、身份证号等敏感信息的文本进行简单脱敏处理，"
        "降低日志意外泄露用户隐私的风险。"
    ),
    usage=(
        "在任意聊天中使用：\n"
        "  /sanitize 需要脱敏的文本\n"
        "插件会返回一个经过基础脱敏后的版本，可用来验证规则是否符合预期，"
        "也可以作为实现日志过滤器时的参考实现。"
    ),
    version="1.0.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/log_sanitizer",
    keywords=["privacy", "log", "sanitizer", "脱敏", "日志", "安全"],
    extra={
        "plugin_type": "system",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    },
    python_dependencies=[],
)


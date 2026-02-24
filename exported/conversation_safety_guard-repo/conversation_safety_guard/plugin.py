"""
Conversation Safety Guard Plugin

一个轻量级的情绪分析与安全建议插件示例。

特点：
- 不依赖外部机器学习库，只用简单关键词和规则做基础情绪判断；
- 通过 PlusCommand 形式提供 `/mood` 指令，新手也易于阅读与二次开发；
- 你可以在此基础上接入更先进的情绪分析 API 或大模型调用。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


class MoodCheckCommand(PlusCommand):
    """对一段文本做情绪倾向分析，并给出安全建议。"""

    command_name: str = "mood"
    command_description: str = "分析一段话的情绪倾向并给出安全建议"
    command_aliases: ClassVar[list[str]] = ["心情检测", "情绪分析"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 20

    @require_permission("use", deny_message="❌ 你没有权限使用情绪分析功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        """
        执行命令。

        使用示例：
          /mood 我最近压力有点大，总是睡不着
        """
        text = (args.raw_args or "").strip()
        if not text:
            await self.send_text("请在指令后面加上一段需要分析的文本，例如：/mood 我最近有点累。")
            return True, None, False

        category, score = self._classify_emotion(text)
        suggestion = self._build_suggestion(category)

        reply = (
            "🧠 情绪检测结果：\n"
            f"- 粗略判断：{category}\n"
            f"- 情绪强度：{int(score * 100)} / 100\n\n"
            f"💡 建议：{suggestion}\n\n"
            "⚠️ 说明：\n"
            "本功能仅基于关键词进行简单判断，不构成专业意见；"
            "如果你正处于严重的情绪困扰或危险境地，请优先联系身边可信任的人或专业机构。"
        )
        await self.send_text(reply)
        return True, "已返回情绪分析结果", True

    def _classify_emotion(self, text: str) -> tuple[str, float]:
        """非常简单的基于关键词的情绪分类逻辑。"""
        lowered = text.lower()

        negative_keywords = [
            "难受",
            "抑郁",
            "不想活",
            "失眠",
            "累",
            "烦",
            "崩溃",
            "痛苦",
            "绝望",
            "孤独",
        ]
        danger_keywords = [
            "自杀",
            "结束生命",
            "想死",
            "轻生",
        ]
        positive_keywords = [
            "开心",
            "高兴",
            "不错",
            "很好",
            "还行",
            "满足",
            "幸福",
        ]

        score = 0.5
        category = "情绪中性 / 难以判断"

        if any(k in lowered for k in danger_keywords):
            category = "可能存在较高风险的负面情绪"
            score = 0.95
        elif any(k in lowered for k in negative_keywords):
            category = "偏消极 / 低落情绪"
            score = 0.8
        elif any(k in lowered for k in positive_keywords):
            category = "偏积极 / 正向情绪"
            score = 0.8

        return category, score

    def _build_suggestion(self, category: str) -> str:
        """根据情绪类别给出简单的建议文字。"""
        if "高风险" in category:
            return (
                "我非常在意你的感受。建议优先联系现实生活中信任的人，"
                "例如家人、朋友，或本地的专业心理援助热线；"
                "在网络环境中，我会尽量用温和方式陪你聊聊，但无法替代专业帮助。"
            )
        if "偏消极" in category:
            return (
                "可以适当给自己一点空间和时间，尝试把压力拆分成更小的问题逐步解决，"
                "也可以和信任的人分享你的感受，让情绪不要闷在心里。"
            )
        if "偏积极" in category:
            return "看起来你现在的状态还不错，可以尝试记录下让你开心的事情，在艰难的时候回想一下。"
        return "目前难以准确判断你的情绪，但无论如何，你的感受是重要的，可以多聊聊让你在意的事情。"


@register_plugin
class ConversationSafetyGuardPlugin(BasePlugin):
    """
    插件入口类。

    当前版本仅通过 PlusCommand 提供功能，
    不会自动拦截所有对话内容，适合作为安全工具箱组件。
    """

    plugin_name: str = "conversation_safety_guard"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(MoodCheckCommand.get_plus_command_info(), MoodCheckCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /mood 情绪分析指令",
        )
    ]

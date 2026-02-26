"""
轻量 FAQ 与知识库增强插件

一个非常轻量的 FAQ / 知识库插件示例。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import FAQConfig
from .handlers import FAQManager


class FAQCommand(PlusCommand):
    """查询轻量 FAQ / 知识库"""

    command_name: str = "faq"
    command_description: str = "从轻量 FAQ/知识库中查找常见问题的标准答案"
    command_aliases: ClassVar[list[str]] = ["常见问题", "帮助查询"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    def __init__(self):
        super().__init__()
        self.config = FAQConfig()
        self.manager = FAQManager(
            faq_entries=self.config.BUILT_IN_FAQ,
            match_threshold=self.config.match_threshold
        )

    @require_permission("use", deny_message="❌ 你没有权限使用 FAQ 查询功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        query = (args.raw_args or "").strip()
        if not query:
            await self.send_text(
                "请在指令后面带上要查询的关键字，例如：/faq 帮助\n"
                "你也可以尝试：/faq 插件 列表、/faq 报错 反馈 等。"
            )
            return True, None, False

        entry = self.manager.find_best_match(query)
        if not entry:
            await self.send_text(
                "暂时没有找到与你问题足够接近的 FAQ 条目。\n"
                "你可以尝试换个关键词，或者直接向维护者反馈你的问题。"
            )
            return True, None, False

        reply = f"📚 FAQ 匹配结果：\n\n❓ {entry.question}\n\n💡 标准答案：\n{entry.answer}"
        await self.send_text(reply)
        return True, "已返回 FAQ 查询结果", True


@register_plugin
class SimpleFAQKnowledgePlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "simple_faq_knowledge"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(FAQCommand.get_plus_command_info(), FAQCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /faq 指令查询轻量 FAQ / 知识库",
        )
    ]


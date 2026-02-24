"""
Simple FAQ / Knowledge Plugin

一个非常轻量的 FAQ / 知识库插件示例。

特点：
- 使用纯 Python 字典维护问答条目，新手可以直接在代码里添加或修改；
- 使用简单的“关键词匹配 + 相似度评分”来找到最合适的标准答案；
- 通过 `/faq` 指令调用，不会改变现有对话流程。
"""

from dataclasses import dataclass
from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


@dataclass
class FAQEntry:
    question: str
    keywords: list[str]
    answer: str


# 你可以根据自己的 Bot 使用场景把这里的条目改成自己的常见问题
BUILT_IN_FAQ: list[FAQEntry] = [
    FAQEntry(
        question="如何查看当前可用插件？",
        keywords=["插件", "列表", "可用", "启用", "关闭"],
        answer=(
            "你可以在 MoFox-Bot 的管理面板或配置文件中查看当前加载的插件列表；"
            "如果你在使用第三方插件仓库，请确认对应仓库已被正确加入到 plugins.json 中。"
        ),
    ),
    FAQEntry(
        question="如何获取帮助或查看常用指令？",
        keywords=["帮助", "指令", "命令", "help"],
        answer=(
            "可以尝试发送 `/help` 或在项目文档中查找“常用指令”章节；"
            "不同部署可能有不同的指令集合，具体以管理员提供的说明为准。"
        ),
    ),
    FAQEntry(
        question="遇到问题应该如何反馈？",
        keywords=["问题", "反馈", "bug", "报错", "错误"],
        answer=(
            "建议先截图或复制出错信息，记录出现问题的大致时间和操作步骤，"
            "然后发送给 Bot 的维护者或在对应的 GitHub 仓库中提 issue。"
        ),
    ),
]


def _similarity(a: str, b: str) -> float:
    """
    一个非常简单的相似度函数：
    - 把字符串转为小写
    - 计算共同出现的字符种类比例
    """
    if not a or not b:
        return 0.0
    sa = set(a.lower())
    sb = set(b.lower())
    inter = len(sa & sb)
    union = len(sa | sb)
    if union == 0:
        return 0.0
    return inter / union


def find_best_faq(query: str) -> FAQEntry | None:
    """在内置 FAQ 列表中找到与 query 最接近的一条。"""
    best_entry: FAQEntry | None = None
    best_score = 0.0
    for entry in BUILT_IN_FAQ:
        # 关键词命中加成
        kw_score = 0.0
        for kw in entry.keywords:
            if kw in query:
                kw_score += 0.3
        sim_score = _similarity(query, entry.question) + kw_score
        if sim_score > best_score:
            best_score = sim_score
            best_entry = entry
    # 设定一个最低阈值，避免误匹配
    if best_score < 0.2:
        return None
    return best_entry


class FAQCommand(PlusCommand):
    """查询轻量 FAQ / 知识库。"""

    command_name: str = "faq"
    command_description: str = "从轻量 FAQ/知识库中查找常见问题的标准答案"
    command_aliases: ClassVar[list[str]] = ["常见问题", "帮助查询"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    @require_permission("use", deny_message="❌ 你没有权限使用 FAQ 查询功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        """
        执行命令。

        示例：
          /faq 帮助
          /faq 插件 列表
        """
        query = (args.raw_args or "").strip()
        if not query:
            await self.send_text(
                "请在指令后面带上要查询的关键字，例如：/faq 帮助\n"
                "你也可以尝试：/faq 插件 列表、/faq 报错 反馈 等。"
            )
            return True, None, False

        entry = find_best_faq(query)
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
    """插件入口类。"""

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

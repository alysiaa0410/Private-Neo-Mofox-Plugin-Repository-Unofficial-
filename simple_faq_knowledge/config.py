"""FAQ插件配置"""

from dataclasses import dataclass


@dataclass
class FAQEntry:
    """FAQ条目"""
    question: str
    keywords: list[str]
    answer: str


class FAQConfig:
    """FAQ配置"""
    
    # 内置FAQ条目
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
                "可以尝试发送 `/help` 或在项目文档中查找"常用指令"章节；"
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
    
    # 匹配阈值
    match_threshold: float = 0.2


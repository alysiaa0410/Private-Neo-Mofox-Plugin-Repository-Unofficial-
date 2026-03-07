"""情绪分析插件配置"""

from dataclasses import dataclass, field


@dataclass
class SafetyConfig:
    """情绪分析配置"""
    
    # 负面情绪关键词
    negative_keywords: list[str] = field(default_factory=lambda: [
        "难受", "抑郁", "不想活", "失眠", "累", "烦", "崩溃", "痛苦", "绝望", "孤独"
    ])
    
    # 危险情绪关键词
    danger_keywords: list[str] = field(default_factory=lambda: [
        "自杀", "结束生命", "想死", "轻生"
    ])
    
    # 积极情绪关键词
    positive_keywords: list[str] = field(default_factory=lambda: [
        "开心", "高兴", "不错", "很好", "还行", "满足", "幸福"
    ])









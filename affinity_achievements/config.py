"""亲密度插件配置"""

from dataclasses import dataclass


@dataclass
class AffinityConfig:
    """亲密度配置"""
    
    # 成就阈值和称号
    achievements = [
        (5, "初次相识"),
        (20, "常来坐坐"),
        (50, "老朋友"),
        (100, "特别熟悉的伙伴"),
        (200, "形影不离的搭子"),
    ]









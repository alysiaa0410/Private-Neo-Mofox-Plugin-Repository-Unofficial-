"""每日签到插件配置"""

from dataclasses import dataclass


@dataclass
class CheckinConfig:
    """签到配置"""
    
    # 连击奖励阈值
    streak_milestones = [3, 7, 14, 30]
    
    # 是否启用持久化存储（当前版本仅内存存储）
    enable_persistence = False









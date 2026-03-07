"""
每日签到插件配置
"""

from typing import ClassVar

from src.core.components.base import BaseConfig
from src.kernel.config.core import Field, SectionBase, config_section


class Config(BaseConfig):
    """每日签到插件配置"""

    config_name: ClassVar[str] = "config"
    config_description: ClassVar[str] = "每日签到插件配置"

    @config_section("general")
    class GeneralSection(SectionBase):
        """通用配置节"""

        enabled: bool = Field(default=True, description="是否启用签到功能")
        
    @config_section("rewards")
    class RewardsSection(SectionBase):
        """奖励配置节"""
        
        milestone_3: str = Field(
            default="已经连续签到 3 天，继续加油，很快就能冲更长的连击纪录！",
            description="3天连击奖励文本"
        )
        milestone_7: str = Field(
            default="连续一周签到！习惯正在成形，坚持就是胜利。",
            description="7天连击奖励文本"
        )
        milestone_14: str = Field(
            default="两周连击达成！保持这个节奏，你和 bot 会越来越熟。",
            description="14天连击奖励文本"
        )
        milestone_30: str = Field(
            default="你已经坚持打卡 30+ 天，太厉害了！给自己一点真实的奖励吧。",
            description="30天连击奖励文本"
        )

    general: GeneralSection = Field(default_factory=GeneralSection)
    rewards: RewardsSection = Field(default_factory=RewardsSection)


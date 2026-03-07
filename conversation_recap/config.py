"""对话回顾插件配置"""

from dataclasses import dataclass


@dataclass
class RecapConfig:
    """回顾配置"""
    
    # 最多回顾的消息数量
    max_messages: int = 30
    
    # 消息预览长度限制
    preview_limit: int = 60









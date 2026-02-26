"""日志脱敏插件配置"""

from dataclasses import dataclass


@dataclass
class SanitizerConfig:
    """脱敏配置"""
    
    # 是否启用手机号脱敏
    enable_phone_mask: bool = True
    
    # 是否启用邮箱脱敏
    enable_email_mask: bool = True
    
    # 是否启用身份证号脱敏
    enable_id_mask: bool = True


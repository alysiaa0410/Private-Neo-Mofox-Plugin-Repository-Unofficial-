"""文本脱敏业务逻辑处理"""

import re


class TextSanitizer:
    """文本脱敏处理器"""
    
    # 正则表达式模式
    PHONE_PATTERN = re.compile(r"(1[3-9]\d{9})")
    EMAIL_PATTERN = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    ID_PATTERN = re.compile(r"\b(\d{6})(\d{8})(\d{3}[0-9Xx])\b")
    
    def __init__(self, enable_phone: bool = True, enable_email: bool = True, enable_id: bool = True):
        self.enable_phone = enable_phone
        self.enable_email = enable_email
        self.enable_id = enable_id
    
    def _mask_phone(self, match: re.Match) -> str:
        """掩码手机号"""
        s = match.group(1)
        return s[:3] + "****" + s[-4:]
    
    def _mask_email(self, match: re.Match) -> str:
        """掩码邮箱"""
        name, domain = match.groups()
        if len(name) <= 2:
            masked = "*" * len(name)
        else:
            masked = name[0] + "*" * (len(name) - 2) + name[-1]
        return masked + "@" + domain
    
    def _mask_id(self, match: re.Match) -> str:
        """掩码身份证号"""
        head, mid, tail = match.groups()
        return head + "********" + tail
    
    def sanitize(self, text: str) -> str:
        """
        对文本进行脱敏处理
        
        Args:
            text: 原始文本
            
        Returns:
            str: 脱敏后的文本
        """
        result = text
        
        if self.enable_phone:
            result = self.PHONE_PATTERN.sub(self._mask_phone, result)
        
        if self.enable_email:
            result = self.EMAIL_PATTERN.sub(self._mask_email, result)
        
        if self.enable_id:
            result = self.ID_PATTERN.sub(self._mask_id, result)
        
        return result


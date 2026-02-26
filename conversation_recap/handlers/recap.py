"""对话回顾业务逻辑处理"""

from datetime import datetime, timedelta
from typing import Any


class RecapHandler:
    """对话回顾处理器"""
    
    def __init__(self, max_messages: int = 30, preview_limit: int = 60):
        self.max_messages = max_messages
        self.preview_limit = preview_limit
    
    def preview_text(self, text: str) -> str:
        """生成文本预览"""
        s = (text or "").strip().replace("\n", " ")
        if len(s) <= self.preview_limit:
            return s
        return s[: self.preview_limit - 3] + "..."
    
    def get_role_prefix(self, role: str) -> str:
        """获取角色前缀"""
        r = (role or "").lower()
        if "user" in r:
            return "你："
        if "assistant" in r or "bot" in r:
            return "Bot："
        return "："
    
    async def fetch_recent_messages(self, message_api, chat_id: str) -> list[dict[str, Any]]:
        """
        尝试从 message_api 获取当前会话的近期消息
        
        优先使用 get_messages_by_chat_id(chat_id, limit)
        若不存在，则退化为 get_messages_by_time(start_time, end_time) 并筛选 chat_id
        """
        getter = getattr(message_api, "get_messages_by_chat_id", None)
        if callable(getter):
            try:
                return await getter(chat_id=chat_id, limit=self.max_messages)
            except TypeError:
                # 部分版本参数名可能不同，尝试位置参数
                return await getter(chat_id, self.max_messages)

        # fallback：按时间拉取后筛选
        now = datetime.now()
        start = now - timedelta(days=1)
        time_getter = getattr(message_api, "get_messages_by_time", None)
        if not callable(time_getter):
            return []

        all_messages = await time_getter(start_time=start.timestamp(), end_time=now.timestamp())
        # 过滤 chat_id
        filtered = [m for m in all_messages if str(m.get("chat_id")) == str(chat_id)]
        return filtered[-self.max_messages :]
    
    def format_messages(self, messages: list[dict[str, Any]]) -> list[str]:
        """格式化消息列表"""
        lines: list[str] = []
        
        for msg in messages:
            content = str(msg.get("content") or "")
            if not content.strip():
                continue
            role = str(msg.get("role") or msg.get("sender") or "")
            lines.append(f"- {self.get_role_prefix(role)} {self.preview_text(content)}")
        
        return lines


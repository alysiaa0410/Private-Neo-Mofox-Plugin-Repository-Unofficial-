"""亲密度业务逻辑处理"""

from dataclasses import dataclass


@dataclass
class AffinityState:
    """亲密度状态"""
    total_messages: int = 0


class AffinityHandler:
    """亲密度处理器"""
    
    def __init__(self, achievements: list[tuple[int, str]]):
        self._user_state: dict[str, AffinityState] = {}
        self.achievements = achievements
    
    def get_user_state(self, user_id: str) -> AffinityState:
        """获取用户亲密度状态"""
        return self._user_state.setdefault(user_id, AffinityState())
    
    def record_message(self, user_id: str) -> None:
        """记录用户消息"""
        state = self.get_user_state(user_id)
        state.total_messages += 1
    
    def get_affinity_info(self, user_id: str) -> dict:
        """
        获取用户亲密度信息
        
        Returns:
            dict: {
                'total_messages': int,
                'current_level': str,
                'unlocked': list[str],
                'next_target': str | None
            }
        """
        state = self.get_user_state(user_id)
        
        level_name = "尚未获得称号"
        unlocked: list[str] = []
        next_target: str | None = None
        
        for threshold, name in self.achievements:
            if state.total_messages >= threshold:
                level_name = name
                unlocked.append(name)
            elif next_target is None:
                next_target = f"{threshold} 条对话解锁「{name}」"
        
        return {
            'total_messages': state.total_messages,
            'current_level': level_name,
            'unlocked': unlocked,
            'next_target': next_target
        }









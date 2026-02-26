"""签到业务逻辑处理"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CheckinState:
    """签到状态"""
    last_checkin_date: str | None = None  # YYYY-MM-DD
    streak_days: int = 0


class CheckinHandler:
    """签到处理器"""
    
    def __init__(self):
        self._states: dict[str, CheckinState] = {}
    
    def get_today_str(self) -> str:
        """获取今天的日期字符串"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_user_state(self, user_id: str) -> CheckinState:
        """获取用户签到状态"""
        return self._states.setdefault(user_id, CheckinState())
    
    def is_checked_in_today(self, user_id: str) -> bool:
        """检查用户今天是否已签到"""
        state = self.get_user_state(user_id)
        return state.last_checkin_date == self.get_today_str()
    
    def do_checkin(self, user_id: str) -> tuple[int, bool]:
        """
        执行签到
        
        Returns:
            tuple[int, bool]: (连击天数, 是否是新签到)
        """
        today = self.get_today_str()
        state = self.get_user_state(user_id)
        
        if state.last_checkin_date == today:
            return state.streak_days, False
        
        # 判断是否连续
        if state.last_checkin_date is not None:
            try:
                last = datetime.strptime(state.last_checkin_date, "%Y-%m-%d").date()
                now = datetime.strptime(today, "%Y-%m-%d").date()
                if (now - last).days == 1:
                    state.streak_days += 1
                else:
                    state.streak_days = 1
            except ValueError:
                state.streak_days = 1
        else:
            state.streak_days = 1
        
        state.last_checkin_date = today
        return state.streak_days, True
    
    def get_bonus_text(self, streak: int) -> str:
        """根据连击天数获取奖励文本"""
        if streak >= 30:
            return "你已经坚持打卡 30+ 天，太厉害了！给自己一点真实的奖励吧。"
        if streak >= 14:
            return "两周连击达成！保持这个节奏，你和 bot 会越来越熟。"
        if streak >= 7:
            return "连续一周签到！习惯正在成形，坚持就是胜利。"
        if streak >= 3:
            return "已经连续签到 3 天，继续加油，很快就能冲更长的连击纪录！"
        return "从今天开始，我们一起养成一个小小的好习惯。"


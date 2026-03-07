"""情绪分析业务逻辑处理"""


class MoodAnalyzer:
    """情绪分析器"""
    
    def __init__(self, negative_keywords: list[str], danger_keywords: list[str], positive_keywords: list[str]):
        self.negative_keywords = negative_keywords
        self.danger_keywords = danger_keywords
        self.positive_keywords = positive_keywords
    
    def classify_emotion(self, text: str) -> tuple[str, float]:
        """
        基于关键词的情绪分类
        
        Returns:
            tuple[str, float]: (情绪类别, 情绪强度分数 0-1)
        """
        lowered = text.lower()
        
        score = 0.5
        category = "情绪中性 / 难以判断"
        
        if any(k in lowered for k in self.danger_keywords):
            category = "可能存在较高风险的负面情绪"
            score = 0.95
        elif any(k in lowered for k in self.negative_keywords):
            category = "偏消极 / 低落情绪"
            score = 0.8
        elif any(k in lowered for k in self.positive_keywords):
            category = "偏积极 / 正向情绪"
            score = 0.8
        
        return category, score
    
    def build_suggestion(self, category: str) -> str:
        """根据情绪类别给出建议"""
        if "高风险" in category:
            return (
                "我非常在意你的感受。建议优先联系现实生活中信任的人，"
                "例如家人、朋友，或本地的专业心理援助热线；"
                "在网络环境中，我会尽量用温和方式陪你聊聊，但无法替代专业帮助。"
            )
        if "偏消极" in category:
            return (
                "可以适当给自己一点空间和时间，尝试把压力拆分成更小的问题逐步解决，"
                "也可以和信任的人分享你的感受，让情绪不要闷在心里。"
            )
        if "偏积极" in category:
            return "看起来你现在的状态还不错，可以尝试记录下让你开心的事情，在艰难的时候回想一下。"
        return "目前难以准确判断你的情绪，但无论如何，你的感受是重要的，可以多聊聊让你在意的事情。"









"""FAQ业务逻辑处理"""

from ..config import FAQEntry


class FAQManager:
    """FAQ管理器"""
    
    def __init__(self, faq_entries: list[FAQEntry], match_threshold: float = 0.2):
        self.faq_entries = faq_entries
        self.match_threshold = match_threshold
    
    def calculate_similarity(self, a: str, b: str) -> float:
        """
        计算两个字符串的相似度
        
        使用简单的字符集合交集比例
        """
        if not a or not b:
            return 0.0
        sa = set(a.lower())
        sb = set(b.lower())
        inter = len(sa & sb)
        union = len(sa | sb)
        if union == 0:
            return 0.0
        return inter / union
    
    def find_best_match(self, query: str) -> FAQEntry | None:
        """
        在FAQ列表中找到与query最接近的一条
        
        Args:
            query: 查询字符串
            
        Returns:
            FAQEntry | None: 最匹配的FAQ条目，如果没有达到阈值则返回None
        """
        best_entry: FAQEntry | None = None
        best_score = 0.0
        
        for entry in self.faq_entries:
            # 关键词命中加成
            kw_score = 0.0
            for kw in entry.keywords:
                if kw in query:
                    kw_score += 0.3
            
            # 计算与问题的相似度
            sim_score = self.calculate_similarity(query, entry.question) + kw_score
            
            if sim_score > best_score:
                best_score = sim_score
                best_entry = entry
        
        # 设定最低阈值，避免误匹配
        if best_score < self.match_threshold:
            return None
        
        return best_entry









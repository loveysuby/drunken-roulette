import random

class QuestionManager:
    def __init__(self):
        # 기본 질문 목록 (한국어로 변경)
        self.questions = [
            "가장 최근에 술 마신 날은?",
            "가장 좋아하는 술은?",
            "술 마시고 가장 창피했던 경험은?",
            "술자리에서 가장 웃겼던 순간은?",
            "술자리에서 절대 하지 않는 것은?",
            "다음 사람에게 건배사를 제안하세요",
            "지금까지 마신 술 중 최고 도수는?",
            "술자리에서 가장 싫어하는 유형은?",
            "술 마시고 한 최악의 결정은?",
            "술자리에서 지켜야 할 예의는?"
        ]
    
    def get_random_question(self):
        """랜덤 질문 반환"""
        return random.choice(self.questions)
    
    def add_question(self, question):
        """새 질문 추가"""
        self.questions.append(question)
        
    def remove_question(self, question):
        """질문 삭제"""
        if question in self.questions:
            self.questions.remove(question)
            return True
        return False

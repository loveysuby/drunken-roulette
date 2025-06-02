import json
import os
import time


class GameManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.players = []
        self.current_player = None
        self.current_question = None
        self.timer_start = 0
        self.timer_duration = 10  # 10초 타이머
        self.load_players()

    def load_players(self):
        """플레이어 데이터 로드"""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.players = json.load(f)
        except Exception as e:
            print(f"플레이어 데이터 로드 실패: {e}")
            self.players = []

    def save_players(self):
        """플레이어 데이터 저장"""
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.players, f, ensure_ascii=False)
        except Exception as e:
            print(f"플레이어 데이터 저장 실패: {e}")

    def add_player(self, name):
        """플레이어 추가"""
        if name and name not in self.players:
            self.players.append(name)
            self.save_players()
            return True
        return False

    def remove_player(self, name):
        """플레이어 제거"""
        if name in self.players:
            self.players.remove(name)
            self.save_players()
            return True
        return False

    def set_current_player(self, player):
        """현재 지목된 플레이어 설정"""
        self.current_player = player

    def set_current_question(self, question):
        """현재 질문 설정"""
        self.current_question = question

    def start_timer(self):
        """타이머 시작"""
        self.timer_start = time.time()

    def get_remaining_time(self):
        """남은 시간 계산"""
        elapsed = time.time() - self.timer_start
        remaining = max(0, self.timer_duration - elapsed)
        return remaining

    def is_time_up(self):
        """시간 초과 여부 확인"""
        return self.get_remaining_time() <= 0

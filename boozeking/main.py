import os
import sys
import pygame
from pygame.locals import *
import time
import platform

# 게임 모듈 임포트
from game.ui import UI
from game.question import QuestionManager
from game.roulette import Roulette
from game.manager import GameManager

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)


# 게임 상태 정의
class GameState:
    MENU = 0
    PLAYER_REGISTRATION = 1
    QUESTION_SELECTION = 2
    ROULETTE = 3
    ANSWER = 4
    RESULT = 5


class JimokwangGame:
    def __init__(self):
        # Pygame 초기화
        pygame.init()
        pygame.display.set_caption("Jimokwang - Drinking Game")

        # 화면 설정
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # 게임 상태 및 리소스 초기화
        self.state = GameState.MENU
        self.running = True

        # 게임 매니저 초기화
        data_path = os.path.join(os.path.dirname(__file__), "data", "players.json")
        self.game_manager = GameManager(data_path)

        # UI 초기화
        self.ui = UI(self.screen)

        # 질문 관리자 초기화
        self.question_manager = QuestionManager()

        # 룰렛 초기화
        self.roulette = Roulette(
            self.screen, self.game_manager.players, self.ui.font_small
        )

        # 입력 필드 관련 변수
        self.input_text = ""
        self.input_active = False

        # 현재 선택된 질문과 플레이어
        self.current_question = None
        self.current_player = None

    def run(self):
        """게임 메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state == GameState.MENU:
                        self.running = False
                    else:
                        self.state = GameState.MENU

                # 입력 필드 활성화 상태에서 텍스트 입력 처리
                if self.input_active:
                    if event.key == K_RETURN:
                        if self.state == GameState.PLAYER_REGISTRATION:
                            if self.input_text:
                                self.game_manager.add_player(self.input_text)
                                self.input_text = ""
                                # 룰렛 플레이어 목록 업데이트
                                self.roulette = Roulette(
                                    self.screen,
                                    self.game_manager.players,
                                    self.ui.font_small,
                                )
                    elif event.key == K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        # 한글 입력을 위한 유니코드 처리
                        if event.unicode:
                            self.input_text += event.unicode

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # 메뉴 화면에서의 버튼 클릭 처리
                if self.state == GameState.MENU:
                    # 시작 버튼 영역 (임시)
                    start_btn_rect = pygame.Rect(300, 200, 200, 50)
                    if start_btn_rect.collidepoint(mouse_pos):
                        if len(self.game_manager.players) > 1:
                            self.state = GameState.QUESTION_SELECTION
                            self.current_question = (
                                self.question_manager.get_random_question()
                            )
                        else:
                            self.state = GameState.PLAYER_REGISTRATION

                    # 플레이어 등록 버튼 영역 (임시)
                    player_btn_rect = pygame.Rect(300, 270, 200, 50)
                    if player_btn_rect.collidepoint(mouse_pos):
                        self.state = GameState.PLAYER_REGISTRATION
                        self.input_active = True

                # 플레이어 등록 화면에서의 버튼 클릭 처리
                elif self.state == GameState.PLAYER_REGISTRATION:
                    # 입력 필드 클릭 처리
                    input_rect = pygame.Rect(250, 200, 300, 40)
                    self.input_active = input_rect.collidepoint(mouse_pos)

                    # 돌아가기 버튼
                    back_btn_rect = pygame.Rect(300, 400, 200, 50)
                    if back_btn_rect.collidepoint(mouse_pos):
                        self.state = GameState.MENU

                    # 시작 버튼 (플레이어가 2명 이상일 때만 활성화)
                    if len(self.game_manager.players) > 1:
                        start_btn_rect = pygame.Rect(300, 330, 200, 50)
                        if start_btn_rect.collidepoint(mouse_pos):
                            self.state = GameState.QUESTION_SELECTION
                            self.current_question = (
                                self.question_manager.get_random_question()
                            )

                    # 플레이어 삭제 버튼 처리
                    if self.game_manager.players:
                        for i, player in enumerate(self.game_manager.players):
                            y_pos = 360 + i * 30
                            if y_pos < self.height - 50:
                                # 삭제 버튼 영역
                                delete_btn_rect = pygame.Rect(250, y_pos - 10, 20, 20)
                                if delete_btn_rect.collidepoint(mouse_pos):
                                    self.game_manager.remove_player(player)
                                    # 룰렛 플레이어 목록 업데이트
                                    self.roulette = Roulette(
                                        self.screen,
                                        self.game_manager.players,
                                        self.ui.font_small,
                                    )
                                    break

                # 질문 선택 화면에서의 버튼 클릭 처리
                elif self.state == GameState.QUESTION_SELECTION:
                    # 다음 버튼
                    next_btn_rect = pygame.Rect(300, 400, 200, 50)
                    if next_btn_rect.collidepoint(mouse_pos):
                        self.state = GameState.ROULETTE
                        self.roulette.start_spin()

                # 룰렛 화면에서의 버튼 클릭 처리
                elif self.state == GameState.ROULETTE:
                    if not self.roulette.spinning and self.roulette.selected_player:
                        # 다음 버튼
                        next_btn_rect = pygame.Rect(300, 500, 200, 50)
                        if next_btn_rect.collidepoint(mouse_pos):
                            self.state = GameState.ANSWER
                            self.current_player = self.roulette.selected_player
                            self.game_manager.set_current_player(self.current_player)
                            self.game_manager.set_current_question(
                                self.current_question
                            )
                            self.game_manager.start_timer()

                # 답변 화면에서의 버튼 클릭 처리
                elif self.state == GameState.ANSWER:
                    # 답변 완료 버튼
                    answer_btn_rect = pygame.Rect(300, 400, 200, 50)
                    if answer_btn_rect.collidepoint(mouse_pos):
                        self.state = GameState.RESULT

                # 결과 화면에서의 버튼 클릭 처리
                elif self.state == GameState.RESULT:
                    # 다음 라운드 버튼
                    next_round_btn_rect = pygame.Rect(300, 400, 200, 50)
                    if next_round_btn_rect.collidepoint(mouse_pos):
                        self.state = GameState.QUESTION_SELECTION
                        self.current_question = (
                            self.question_manager.get_random_question()
                        )

    def update(self):
        """게임 상태 업데이트"""
        if self.state == GameState.ROULETTE:
            self.roulette.update()

        elif self.state == GameState.ANSWER:
            # 타이머 체크
            if self.game_manager.is_time_up():
                self.state = GameState.RESULT

    def render(self):
        """화면 렌더링"""
        self.screen.fill(WHITE)

        # 메뉴 화면
        if self.state == GameState.MENU:
            self.render_menu()

        # 플레이어 등록 화면
        elif self.state == GameState.PLAYER_REGISTRATION:
            self.render_player_registration()

        # 질문 선택 화면
        elif self.state == GameState.QUESTION_SELECTION:
            self.render_question_selection()

        # 룰렛 화면
        elif self.state == GameState.ROULETTE:
            self.render_roulette()

        # 답변 화면
        elif self.state == GameState.ANSWER:
            self.render_answer()

        # 결과 화면
        elif self.state == GameState.RESULT:
            self.render_result()

        pygame.display.flip()

    def render_menu(self):
        """메뉴 화면 렌더링"""
        # 타이틀
        self.ui.draw_text("지목왕", self.ui.font_large, BLACK, self.width // 2, 100)
        self.ui.draw_text(
            "술자리 지목 게임",
            self.ui.font_medium,
            DARK_GRAY,
            self.width // 2,
            150,
        )

        # 버튼
        start_btn_color = GREEN if len(self.game_manager.players) > 1 else GRAY
        start_btn_rect = self.ui.draw_button(
            "게임 시작",
            self.ui.font_medium,
            BLACK,
            start_btn_color,
            self.width // 2,
            225,
            20,
        )
        player_btn_rect = self.ui.draw_button(
            "플레이어 등록",
            self.ui.font_medium,
            BLACK,
            BLUE,
            self.width // 2,
            295,
            20,
        )

        # 등록된 플레이어 표시
        self.ui.draw_text(
            "등록된 플레이어", self.ui.font_small, BLACK, self.width // 2, 370
        )

        if not self.game_manager.players:
            self.ui.draw_text(
                "등록된 플레이어가 없습니다",
                self.ui.font_small,
                DARK_GRAY,
                self.width // 2,
                410,
            )
        else:
            for i, player in enumerate(self.game_manager.players):
                y_pos = 410 + i * 30
                if y_pos < self.height - 50:  # 화면 범위 내에서만 표시
                    self.ui.draw_text(
                        player, self.ui.font_small, BLACK, self.width // 2, y_pos
                    )

    def render_player_registration(self):
        """플레이어 등록 화면 렌더링"""
        # 타이틀
        self.ui.draw_text(
            "플레이어 등록", self.ui.font_large, BLACK, self.width // 2, 100
        )

        # 입력 필드
        input_rect = pygame.Rect(250, 200, 300, 40)
        input_color = GREEN if self.input_active else GRAY
        pygame.draw.rect(self.screen, input_color, input_rect, 2)

        # 입력 텍스트
        input_surface = self.ui.font_small.render(self.input_text, True, BLACK)
        self.screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        # 안내 텍스트
        self.ui.draw_text(
            "이름을 입력하고 Enter 키를 누르세요",
            self.ui.font_small,
            DARK_GRAY,
            self.width // 2,
            260,
        )

        # 버튼
        start_btn_color = GREEN if len(self.game_manager.players) > 1 else GRAY
        start_btn_rect = self.ui.draw_button(
            "게임 시작",
            self.ui.font_medium,
            BLACK,
            start_btn_color,
            self.width // 2,
            330,
            20,
        )
        back_btn_rect = self.ui.draw_button(
            "돌아가기", self.ui.font_medium, BLACK, RED, self.width // 2, 400, 20
        )

        # 등록된 플레이어 표시
        self.ui.draw_text("등록된 플레이어", self.ui.font_small, BLACK, 150, 330)

        if not self.game_manager.players:
            self.ui.draw_text("없음", self.ui.font_small, DARK_GRAY, 150, 360)
        else:
            for i, player in enumerate(self.game_manager.players):
                y_pos = 360 + i * 30
                if y_pos < self.height - 50:  # 화면 범위 내에서만 표시
                    player_text = self.ui.draw_text(
                        player, self.ui.font_small, BLACK, 150, y_pos, center=False
                    )

                    # 삭제 버튼 (X) 추가
                    delete_btn_rect = pygame.Rect(250, y_pos - 10, 20, 20)
                    pygame.draw.rect(self.screen, RED, delete_btn_rect)
                    self.ui.draw_text(
                        "X",
                        self.ui.font_small,
                        WHITE,
                        delete_btn_rect.centerx,
                        delete_btn_rect.centery,
                    )

    def render_question_selection(self):
        """질문 선택 화면 렌더링"""
        # 타이틀
        self.ui.draw_text("랜덤 질문", self.ui.font_large, BLACK, self.width // 2, 100)

        # 질문 표시
        question_rect = pygame.Rect(100, 200, 600, 100)
        pygame.draw.rect(self.screen, GRAY, question_rect, border_radius=10)

        # 질문 텍스트 (여러 줄로 표시)
        if self.current_question:
            self.ui.draw_text(
                self.current_question, self.ui.font_medium, BLACK, self.width // 2, 250
            )

        # 다음 버튼
        next_btn_rect = self.ui.draw_button(
            "룰렛 돌리기", self.ui.font_medium, BLACK, GREEN, self.width // 2, 400, 20
        )

    def render_roulette(self):
        """룰렛 화면 렌더링"""
        # 타이틀 (Y좌표를 조금 위로 조정)
        self.ui.draw_text(
            "누가 대답할까요?", self.ui.font_large, BLACK, self.width // 2, 60
        )

        # 룰렛 그리기 (룰렛 자체의 Y 중심은 roulette.py에서 조정 예정)
        self.roulette.draw()

        # 선택된 플레이어 표시 (Y좌표를 룰렛 하단에 맞게 조정)
        if not self.roulette.spinning and self.roulette.selected_player:
            # 룰렛의 Y 중심과 반지름을 고려하여 Y 위치 계산 (roulette.py와 동기화 필요)
            roulette_bottom_y = self.roulette.center[1] + self.roulette.radius
            self.ui.draw_text(
                f"선택된 플레이어: {self.roulette.selected_player}",
                self.ui.font_medium,
                RED,
                self.width // 2,
                roulette_bottom_y + 40,  # 룰렛 하단에서 약간 아래
            )

            # 다음 버튼 (선택된 플레이어 텍스트 아래에 위치)
            next_btn_rect = self.ui.draw_button(
                "질문 대답하기",
                self.ui.font_medium,
                BLACK,
                GREEN,
                self.width // 2,
                roulette_bottom_y + 90,  # "선택된 플레이어" 텍스트 아래
                20,
            )

    def render_answer(self):
        """답변 화면 렌더링"""
        # 타이틀
        self.ui.draw_text(
            f"{self.current_player}님, 대답해주세요!",
            self.ui.font_large,
            BLACK,
            self.width // 2,
            100,
        )

        # 질문 표시
        question_rect = pygame.Rect(100, 180, 600, 80)
        pygame.draw.rect(self.screen, GRAY, question_rect, border_radius=10)
        self.ui.draw_text(
            self.current_question, self.ui.font_medium, BLACK, self.width // 2, 220
        )

        # 타이머 표시
        remaining = self.game_manager.get_remaining_time()
        timer_color = GREEN if remaining > 3 else RED
        self.ui.draw_text(
            f"남은 시간: {remaining:.1f}초",
            self.ui.font_large,
            timer_color,
            self.width // 2,
            300,
        )

        # 타이머 바 표시
        timer_rect = pygame.Rect(150, 350, 500, 20)
        pygame.draw.rect(self.screen, GRAY, timer_rect)

        progress_width = int(500 * (remaining / 10))
        if progress_width > 0:
            progress_rect = pygame.Rect(150, 350, progress_width, 20)
            pygame.draw.rect(self.screen, timer_color, progress_rect)

        # 답변 완료 버튼
        answer_btn_rect = self.ui.draw_button(
            "답변 완료", self.ui.font_medium, BLACK, BLUE, self.width // 2, 400, 20
        )

    def render_result(self):
        """결과 화면 렌더링"""
        # 타이머가 끝났는지 확인
        time_up = self.game_manager.is_time_up()

        if time_up:
            # 시간 초과 메시지
            self.ui.draw_text(
                "시간 초과!", self.ui.font_large, RED, self.width // 2, 100
            )
            self.ui.draw_text(
                f"{self.current_player}님, 벌칙을 받으세요!",
                self.ui.font_medium,
                BLACK,
                self.width // 2,
                170,
            )
        else:
            # 성공 메시지
            self.ui.draw_text(
                "대답 성공!", self.ui.font_large, GREEN, self.width // 2, 100
            )
            self.ui.draw_text(
                f"{self.current_player}님, 잘 하셨습니다!",
                self.ui.font_medium,
                BLACK,
                self.width // 2,
                170,
            )

        # 질문 표시
        question_rect = pygame.Rect(100, 230, 600, 80)
        pygame.draw.rect(self.screen, GRAY, question_rect, border_radius=10)
        self.ui.draw_text(
            self.current_question, self.ui.font_medium, BLACK, self.width // 2, 270
        )

        # 다음 라운드 버튼
        next_round_btn_rect = self.ui.draw_button(
            "다음 라운드", self.ui.font_medium, BLACK, GREEN, self.width // 2, 400, 20
        )


if __name__ == "__main__":
    game = JimokwangGame()
    game.run()

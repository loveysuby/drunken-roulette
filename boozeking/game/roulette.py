import pygame
import random
import math

# gfxdraw를 사용하려면 import 필요 (선택 사항)
# from pygame import gfxdraw


class Roulette:
    def __init__(self, screen, players, font_small):  # font_small을 인자로 받도록 수정
        self.screen = screen
        self.players = players
        self.font_small = font_small  # UI 모듈의 폰트를 사용
        self.angle = 0
        self.spinning = False
        self.spin_speed = 0
        self.selected_player = None

        # 화면의 너비와 높이
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # 룰렛의 Y 중심 위치 조정 (화면 상단에 가깝게)
        # 타이틀 Y: 60 (font_large 높이 대략 48)
        # 룰렛 상단과 타이틀 사이에 여백 (예: 20px)을 두도록 설정
        # self.radius는 아래에서 정의되므로, 우선 예상 Y 중심을 계산
        # 예상 룰렛 Y 중심: 타이틀 하단(60 + 24) + 여백(20) + 반지름
        # 여기서는 반지름을 먼저 결정하고 중심을 맞추는 것이 더 직관적일 수 있음

        # 룰렛 반지름 설정 (화면 높이와 하단 UI 공간 고려)
        # 하단 UI가 차지할 예상 높이: 텍스트(font_medium ~36px) + 버튼(font_medium ~36px + padding) + 여백들 ~ 150px
        available_height_for_roulette = (
            screen_height - 60 - 150
        )  # 상단 타이틀 영역과 하단 UI 영역 제외
        self.radius = min(
            screen_width // 3, available_height_for_roulette // 2 - 20
        )  # 위아래 여백 20px 추가 고려
        self.radius = max(50, self.radius)  # 최소 반지름 보장

        # 룰렛 중심 Y좌표: 타이틀 하단 + 룰렛 반지름 + 상단 여백
        title_bottom_y = (
            60 + self.font_small.get_height() // 2
        )  # 대략적인 타이틀 하단 (font_large 기준이 더 정확할 수 있음)
        self.center = (
            screen_width // 2,
            title_bottom_y + self.radius + 30,  # 타이틀과 룰렛 사이 여백 30px
        )

    def start_spin(self):
        """룰렛 회전 시작"""
        self.spinning = True
        self.spin_speed = random.uniform(10, 20)  # 초기 회전 속도
        self.selected_player = None

    def update(self):
        """룰렛 상태 업데이트"""
        if self.spinning:
            self.angle += self.spin_speed
            self.spin_speed *= 0.98  # 점차 감속

            if self.spin_speed < 0.1:
                self.spinning = False
                self.select_player()

    def select_player(self):
        """룰렛이 멈추면 플레이어 선택"""
        if not self.players:
            return None

        segment_angle = 360 / len(self.players)
        normalized_angle = self.angle % 360
        selected_index = int(normalized_angle / segment_angle)
        self.selected_player = self.players[selected_index]
        return self.selected_player

    def draw(self):
        """룰렛 그리기"""
        if not self.players:
            # 플레이어가 없을 경우 안내 문구 표시
            text = self.font_small.render(
                "플레이어를 등록해주세요", True, (100, 100, 100)
            )
            text_rect = text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
            )
            self.screen.blit(text, text_rect)
            return

        # 룰렛 배경 원 그리기 (테두리 효과를 위해 약간 더 크게)
        # pygame.draw.circle(self.screen, (50, 50, 50), self.center, self.radius + 3) # 어두운 테두리
        # pygame.draw.circle(self.screen, (220, 220, 220), self.center, self.radius) # 밝은 배경

        num_segments = len(self.players)
        segment_angle_degrees = 360 / num_segments

        # 다양한 색상 팔레트 (플레이어 수에 따라 유연하게 선택)
        base_colors = [
            (255, 100, 100),
            (100, 255, 100),
            (100, 100, 255),
            (255, 255, 100),
            (255, 100, 255),
            (100, 255, 255),
            (255, 150, 50),
            (150, 50, 255),
            (50, 255, 150),
        ]
        colors = [base_colors[i % len(base_colors)] for i in range(num_segments)]

        for i, player in enumerate(self.players):
            # 각 세그먼트의 시작 각도와 끝 각도 (도 단위)
            start_angle_deg = self.angle + i * segment_angle_degrees
            end_angle_deg = self.angle + (i + 1) * segment_angle_degrees

            # 부채꼴을 그리기 위한 점들 계산
            points = [self.center]
            # 호를 따라 점들을 추가 (더 부드러운 곡선을 위해 점 개수 늘릴 수 있음)
            for angle_deg in range(
                int(start_angle_deg), int(end_angle_deg) + 1, 1
            ):  # 1도 간격으로 점 생성
                rad = math.radians(angle_deg)
                x = self.center[0] + int(self.radius * math.cos(rad))
                y = self.center[1] + int(self.radius * math.sin(rad))
                points.append((x, y))
            points.append(self.center)  # 부채꼴을 닫기 위해 중앙점 다시 추가

            if len(points) > 2:  # 다각형을 그리려면 최소 3개의 점 필요
                pygame.draw.polygon(self.screen, colors[i], points)
                # 경계선 추가 (검은색)
                pygame.draw.lines(self.screen, (0, 0, 0), False, points, 2)

            # 플레이어 이름 표시 (회전하지 않도록 수정)
            # 텍스트를 부채꼴의 중간 각도, 바깥쪽에 가깝게 위치
            text_angle_rad = math.radians(start_angle_deg + segment_angle_degrees / 2)
            text_radius_factor = 0.7  # 텍스트 위치 (0.0 ~ 1.0, 1.0은 가장자리)

            name_x = self.center[0] + int(
                self.radius * text_radius_factor * math.cos(text_angle_rad)
            )
            name_y = self.center[1] + int(
                self.radius * text_radius_factor * math.sin(text_angle_rad)
            )

            # 텍스트 렌더링
            text_surface = self.font_small.render(
                player, True, (0, 0, 0)
            )  # 검은색 텍스트

            # 텍스트 회전 (선택 사항, 가독성 고려)
            # rotated_text = pygame.transform.rotate(text_surface, -(start_angle_deg + segment_angle_degrees / 2) - 90)
            # text_rect = rotated_text.get_rect(center=(name_x, name_y))
            # self.screen.blit(rotated_text, text_rect)

            # 회전하지 않는 텍스트
            text_rect = text_surface.get_rect(center=(name_x, name_y))
            self.screen.blit(text_surface, text_rect)

        # 화살표 그리기 (룰렛 상단 중앙에 위치하도록 수정)
        arrow_color = (0, 0, 0)  # 검은색 화살표
        arrow_size = 15  # 화살표 크기
        # 화살표 꼭지점: 룰렛 원의 최상단보다 약간 위에 위치
        arrow_tip_y = self.center[1] - self.radius - 5
        arrow_points = [
            (self.center[0], arrow_tip_y - arrow_size),  # 위쪽 꼭지점
            (self.center[0] - arrow_size // 2, arrow_tip_y),  # 왼쪽 아래 꼭지점
            (self.center[0] + arrow_size // 2, arrow_tip_y),  # 오른쪽 아래 꼭지점
        ]
        pygame.draw.polygon(self.screen, arrow_color, arrow_points)

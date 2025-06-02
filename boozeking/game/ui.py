import pygame
import os


class UI:
    def __init__(self, screen):
        self.screen = screen

        # 폰트 파일 경로 설정 (game/fonts 디렉토리 안에 폰트 파일이 있다고 가정)
        font_path = os.path.join(
            os.path.dirname(__file__), "fonts", "NanumGothic.ttf"
        )  # 예시 폰트 파일명

        try:
            # 폰트 파일 직접 로드
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 36)
            self.font_small = pygame.font.Font(font_path, 24)
        except pygame.error as e:
            print(f"폰트 로드 오류: {e}")
            # 폰트 로드에 실패한 경우, 시스템 기본 폰트 사용 (한글 지원 안될 수 있음)
            try:
                # macOS에서 주로 사용되는 한글 폰트들
                available_fonts = [
                    "AppleGothic",
                    "AppleSDGothicNeo-Regular",
                    "NanumGothic",
                    "NanumBarunGothic",
                    "Arial Unicode MS",
                    "Arial",
                ]

                # 사용 가능한 폰트 찾기
                self.font_name = None
                for font_name_system in available_fonts:
                    if (
                        font_name_system in pygame.font.get_fonts()
                        or os.path.exists(f"/Library/Fonts/{font_name_system}.ttf")
                        or os.path.exists(
                            f"/System/Library/Fonts/{font_name_system}.ttf"
                        )
                    ):
                        self.font_name = font_name_system
                        break

                if not self.font_name:
                    self.font_name = pygame.font.get_default_font()

                self.font_large = pygame.font.SysFont(self.font_name, 48)
                self.font_medium = pygame.font.SysFont(self.font_name, 36)
                self.font_small = pygame.font.SysFont(self.font_name, 24)
            except:
                # 시스템 폰트도 실패하면 Pygame 기본 폰트 사용
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 36)
                self.font_small = pygame.font.Font(None, 24)

    def draw_text(self, text, font, color, x, y, center=True):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_button(self, text, font, text_color, button_color, x, y, padding=10):
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        button_rect = pygame.Rect(
            0, 0, text_rect.width + padding * 2, text_rect.height + padding * 2
        )
        button_rect.center = (x, y)

        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)
        self.screen.blit(text_surface, text_rect)

        return button_rect

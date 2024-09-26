import pygame
import color
from ai import AI

def draw_gradient_rect(surface, color1, color2, rect):
    """Draw a gradient rectangle."""
    x, y, w, h = rect
    for i in range(h):
        # Calculate the color at this point
        r = color1[0] + (color2[0] - color1[0]) * i // h
        g = color1[1] + (color2[1] - color1[1]) * i // h
        b = color1[2] + (color2[2] - color1[2]) * i // h
        pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))


class GameControl:
    def __init__(self, screen, font, typeChess,player_name,board):
        # Thông số cần thiết
        self.screen = screen
        self.font = font
        self.board = board

        # Thông tin người chơi
        self.player_name = player_name  # Tên người chơi
        self.player_score = 0  # Số quân ăn được của người chơi
        self.ai_score = 0  # Số quân ăn được của AI
        self.typeChess = typeChess # Quân cờ của người chơi

        # Thông tin đối tượng hiển thị
        self.skip_button_rect = pygame.Rect(610, 480, 180, 50)  # Nút skip
        self.surrender_button_rect = pygame.Rect(610, 540, 180, 50)  # Nút đầu hàng
        self.exit_button_rect = pygame.Rect(250, 350, 100, 50) # Nút thoát
        self.replay_button_rect = pygame.Rect(450, 350, 100, 50) # Nút chơi lại

    def getExitButton(self):
        return self.exit_button_rect
    
    def getReplayButton(self):
        return self.replay_button_rect

    def getSkipButton(self):
        return self.skip_button_rect

    def getSurrenderButton(self):
        return self.surrender_button_rect

    def draw_scoreboard(self, height):

        player_chess, ai_chess = color.WHITE, color.BLACK
        if self.typeChess == -1:
            player_chess, ai_chess = color.BLACK, color.WHITE

        # Vẽ khung bên trái
        draw_gradient_rect(self.screen, color.LIGHT_CYAN, color.DARK_CYAN, (600, 0, 200, height))

        # Hiển thị tên người chơi
        player_text = self.font.render(self.player_name, True, color.BLACK)
        self.screen.blit(player_text, (610, 10))

        # Hiển thị số quân ăn được của người chơi
        score_text = self.font.render(f": {self.player_score}", True, color.BLACK)
        pygame.draw.circle(self.screen, player_chess, (630, 65), 14)  # icon quân cờ
        self.screen.blit(score_text, (650, 50))

        # Hiển thị AI
        player_text = self.font.render("AI Sk follow me", True, color.BLACK)
        self.screen.blit(player_text, (610, 390))

        # Hiển thị số quân ăn được của AI
        ai_score_text = self.font.render(f": {self.ai_score}", True, color.BLACK)
        pygame.draw.circle(self.screen, ai_chess, (630, 445), 14)  # icon quân cờ
        self.screen.blit(ai_score_text, (650, 430))

        turn_text = self.font.render(f"Turn: {self.board.current_turn}", True, color.BLACK)
        self.screen.blit(turn_text, (610, 230))
    
        pygame.draw.rect(self.screen, color.DARK_GRAY, self.skip_button_rect)
        skip_text = self.font.render("Bo qua", True, color.WHITE)
        skip_text_rect = skip_text.get_rect(center=self.skip_button_rect.center)
        self.screen.blit(skip_text, skip_text_rect)

        # Vẽ nút "Đầu hàng"
        pygame.draw.rect(self.screen, color.DARK_RED, self.surrender_button_rect)
        surrender_text = self.font.render("Dau hang", True, color.WHITE)
        surrender_text_rect = surrender_text.get_rect(center=self.surrender_button_rect.center)
        self.screen.blit(surrender_text, surrender_text_rect)

    def draw_game_over_dialog(self):
        screen = self.screen
        font = self.font

        # Hiển thị hộp thoại điểm của bạn
        pygame.draw.rect(screen, color.LIGHT_GRAY, (200, 150, 400, 300))
        score_text = font.render(f"Your score: {self.player_score}", True, color.BLACK)
        screen.blit(score_text, (250, 200))
        ai_score_text = font.render(f"AI score: {self.ai_score}", True, color.BLACK)
        screen.blit(ai_score_text, (250, 250))

        # Vẽ nút "Thoát"
        pygame.draw.rect(screen, color.DARK_RED, self.exit_button_rect)
        exit_text = font.render("Exit", True, color.WHITE)
        screen.blit(exit_text, (270, 360))

        # Vẽ nút "Chơi lại"
        pygame.draw.rect(screen, color.DARK_GREEN, self.replay_button_rect)
        replay_text = font.render("Play Again", True, color.WHITE)
        screen.blit(replay_text, (460, 360))
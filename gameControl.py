import pygame
import color

class GameControl:
    def __init__(self, screen, font, typeChess):
        # Thông số cần thiết
        self.screen = screen
        self.font = font
        # Thông tin người chơi
        self.player_name = "Player name"
        self.player_score = 0  # Số quân ăn được của người chơi
        self.ai_score = 0  # Số quân ăn được của AI
        self.typeChess = typeChess

    def draw_scoreboard(self, height):

        player_chess, ai_chess = color.WHITE, color.BLACK
        if(self.typeChess == -1):
            player_chess, ai_chess = color.BLACK, color.WHITE

        # Vẽ khung bên trái
        pygame.draw.rect(self.screen, color.GRAY, (600, 0, 200, height))

         # Hiển thị tên người chơi
        player_text = self.font.render(self.player_name, True, color.BLACK)
        self.screen.blit(player_text, (610, 30))

        # Hiển thị số quân ăn được của người chơi
        score_text = self.font.render(f": {self.player_score}", True, color.BLACK)
        pygame.draw.circle(self.screen, player_chess, (630, 85), 14) # icon quân cờ
        self.screen.blit(score_text, (650, 70))

         # Hiển thị AI
        player_text = self.font.render("AI Sk follow me", True, color.BLACK)
        self.screen.blit(player_text, (610, 410))

        # Hiển thị số quân ăn được của AI
        ai_score_text = self.font.render(f": {self.ai_score}", True, color.BLACK)
        pygame.draw.circle(self.screen, ai_chess, (630, 465), 14) # icon quân cờ
        self.screen.blit(ai_score_text, (650, 450))
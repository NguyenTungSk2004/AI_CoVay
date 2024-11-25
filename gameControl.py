import pygame
import color
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
    def __init__(self, screen, font, typeChess, player_name, board):
        # Thông số cần thiết
        self.screen = screen
        self.font = font
        self.board = board

        # Thông tin người chơi
        self.player_name = player_name  # Tên người chơi
        self.player_score = 0  # Khởi tạo điểm người chơi bằng 0
        self.ai_score = 0  # Khởi tạo điểm AI bằng 0
        self.typeChess = typeChess # Quân cờ của người chơi
        self.first_move_made = False  # Biến đánh dấu nước đi đầu tiên

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

    def update_scores(self):
        """Cập nhật điểm số từ bảng"""
        if self.typeChess == 1:
            self.player_score = self.board.whoIsWinner()[0]
            self.ai_score = self.board.whoIsWinner()[1]
        else:
            self.player_score = self.board.whoIsWinner()[1]
            self.ai_score = self.board.whoIsWinner()[0]
    
    def set_first_move_made(self):
        """Đánh dấu đã có nước đi đầu tiên"""
        self.first_move_made = True

    def draw_scoreboard(self, height):
        # Cập nhật điểm số trước khi vẽ
        self.update_scores()
        
        player_chess, ai_chess = color.WHITE, color.BLACK
        if self.typeChess == -1:
            player_chess, ai_chess = color.BLACK, color.WHITE

        # Vẽ khung bên trái
        draw_gradient_rect(self.screen, color.LIGHT_BROWN, color.DARK_BROWN, (600, 0, 200, height))

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
        # Cập nhật điểm số cuối cùng
        self.update_scores()
        
        screen = self.screen
        font = self.font

        # Vẽ khung ngoài màu xám đậm
        outer_rect = pygame.Rect(180, 130, 440, 340)
        pygame.draw.rect(screen, (60, 60, 60), outer_rect)  # Xám đậm
        
        # Vẽ khung trong với gradient xám
        inner_rect = pygame.Rect(190, 140, 420, 320)
        draw_gradient_rect(screen, (120, 120, 120), (80, 80, 80), inner_rect)  # Gradient từ xám nhạt đến xám đậm

        # Sử dụng font Emulogic cho Game Over với size nhỏ hơn
        try:
            game_over_font = pygame.font.Font("Emulogic.ttf", 30)  # Giảm size xuống 30
            title_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        except:
            # Fallback nếu không tìm thấy file font
            game_over_font = pygame.font.Font(None, 50)  # Giảm size tương ứng cho font mặc định
            title_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 180))
        screen.blit(title_text, title_rect)

        # Xác định người chiến thắng
        winner_text = ""
        if self.player_score > self.ai_score:
            winner_text = f"{self.player_name} Win!"
        elif self.player_score < self.ai_score:
            winner_text = "AI Win!"
        else:
            winner_text = "Draw!"

        # Hiển thị người chiến thắng với màu nổi bật
        winner_surface = font.render(winner_text, True, (0, 0, 255))  # Giữ nguyên màu xanh dương
        winner_rect = winner_surface.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(winner_surface, winner_rect)

        # Hiển thị điểm số với màu vàng nhạt để nổi bật trên nền xám
        score_text = font.render(f"Your score: {self.player_score}", True, (255, 255, 150))  # Màu vàng nhạt
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(score_text, score_rect)
        
        ai_score_text = font.render(f"AI score: {self.ai_score}", True, (255, 255, 150))  # Màu vàng nhạt
        ai_score_rect = ai_score_text.get_rect(center=(screen.get_width() // 2, 340))
        screen.blit(ai_score_text, ai_score_rect)

        # Vẽ các nút với vị trí và kích thước mới
        # Nút "Thoát"
        exit_text = font.render("Exit", True, color.WHITE)
        self.exit_button_rect = pygame.Rect(250, 380, exit_text.get_width() + 40, 50)
        pygame.draw.rect(screen, color.DARK_RED, self.exit_button_rect)
        exit_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        screen.blit(exit_text, exit_rect)

        # Nút "Chơi lại"
        replay_text = font.render("Play Again", True, color.WHITE)
        self.replay_button_rect = pygame.Rect(450, 380, replay_text.get_width() + 40, 50)
        pygame.draw.rect(screen, color.DARK_GREEN, self.replay_button_rect)
        replay_rect = replay_text.get_rect(center=self.replay_button_rect.center)
        screen.blit(replay_text, replay_rect)
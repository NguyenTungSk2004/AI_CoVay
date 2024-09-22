import pygame

class Board:
    def __init__(self, size,img, spacing_x, spacing_y, chessStart):
        self.size = size
        self.board = [[0] * self.size for _ in range(self.size)]
        self.current_turn = "Player"
        self.image = pygame.image.load(img)  # Tải hình nền bàn cờ
        self.image = pygame.transform.scale(self.image, (600, 600))  # Thay đổi kích thước hình nền
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.chessStart = chessStart

    def draw(self, screen):
        # Vẽ hình nền
        screen.blit(self.image, (0, 0))
        # Vẽ các quân cờ
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    pygame.draw.circle(screen, (255, 255, 255), (x * self.spacing_x + self.chessStart, y * self.spacing_y + self.chessStart), 12)
                elif self.board[x][y] == -1:
                    pygame.draw.circle(screen, (0, 0, 0), (x * self.spacing_x + self.chessStart, y * self.spacing_y + self.chessStart), 12)

    def player_move(self, pos):
        # Lấy tọa độ chuột
        mouse_x, mouse_y = pos

        # Tính toán tọa độ ô gần nhất
        x = round(mouse_x / 30) -1 # Làm tròn tọa độ x
        y = round(mouse_y / 30) -1 # Làm tròn tọa độ y

        # Kiểm tra ô trống
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
            self.board[x][y] = 1  # Giả sử người chơi là quân trắng
            print(f"Player move: {x+1}, {y+1}")
            self.current_turn = "AI"


    def ai_move(self, move):
        # Đánh dấu nước đi của AI
        if move:
            x, y = move
            self.board[x][y] = -1  # Giả sử AI là quân đen
            self.current_turn = "Player"

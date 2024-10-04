import pygame
import color
from rules import Rules
from KO_rule import KO_rule
class Board:
    def __init__(self, MyBoard, typeChess):
        self.size = MyBoard[0]
        self.board = [[0] * self.size for _ in range(self.size)]
        self.image = pygame.image.load(MyBoard[1])  # Tải hình nền bàn cờ
        self.image = pygame.transform.scale(self.image, (600, 600))  # Thay đổi kích thước hình nền
        self.spacing = MyBoard[2]
        self.chessStart = MyBoard[3]
        self.chessSize = MyBoard[4]
        self.typeChess = typeChess
        self.KO_rule = KO_rule()
        
        if (typeChess == -1 ): 
            self.current_turn = "Player"
        else : 
            self.current_turn = "AI"

    def draw(self, screen):
        # Vẽ hình nền
        screen.blit(self.image, (0, 0))
        # Vẽ các quân cờ
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    pygame.draw.circle(screen, color.WHITE, (x * self.spacing + self.chessStart, y * self.spacing + self.chessStart), self.chessSize)
                elif self.board[x][y] == -1:
                    pygame.draw.circle(screen, color.BLACK, (x * self.spacing + self.chessStart, y * self.spacing + self.chessStart), self.chessSize)

    def player_move(self, pos):
        # Lấy tọa độ chuột
        mouse_x, mouse_y = pos
        
        # Tính toán tọa độ ô gần nhất
        x = round((mouse_x - self.chessStart )/ self.spacing)  # Làm tròn tọa độ x
        y = round((mouse_y - self.chessStart) / self.spacing) # Làm tròn tọa độ y

        # Kiểm tra ô trống
        if Rules.is_valid_move(self.board, x, y,self.typeChess) and self.KO_rule.is_repeated_state(self.board,x,y,self.typeChess):
            self.current_turn = "AI"
            self.board[x][y] = self.typeChess
            Rules.capture_stones(self.board,-self.typeChess)
        
    def ai_move(self, move):
        # Đánh dấu nước đi của AI
        if move:
            x, y = move
            if Rules.is_valid_move(self.board,x,y,-self.typeChess) and self.KO_rule.is_repeated_state(self.board,x,y,self.typeChess):
                self.current_turn = "Player"
                self.board[x][y] = -self.typeChess  
                Rules.capture_stones(self.board,self.typeChess)

    
    def test_ai_click(self, move):
        # Đánh dấu nước đi của AI
        if move:
            # Lấy tọa độ chuột
            mouse_x, mouse_y = move
            
            # Tính toán tọa độ ô gần nhất
            x = round((mouse_x - self.chessStart )/ self.spacing)  # Làm tròn tọa độ x
            y = round((mouse_y - self.chessStart) / self.spacing) # Làm tròn tọa độ y

            if Rules.is_valid_move(self.board, x, y,-self.typeChess) and self.KO_rule.is_repeated_state(self.board,x,y,self.typeChess):
                self.current_turn = "Player"
                self.board[x][y] = -self.typeChess  
                Rules.capture_stones(self.board,self.typeChess)
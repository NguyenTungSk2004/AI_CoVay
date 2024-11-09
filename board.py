import pygame
import color
from rules import Rules
from ai import AI
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
        self.rule = Rules()
        self.ai = AI()

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
        suicidal = self.rule.is_suicidal(self.board, x, y,self.typeChess)
        repeated_state = self.rule.is_repeated_state(self.board,x,y,self.typeChess)
        if suicidal and repeated_state:
            self.current_turn = "AI"
            self.board[x][y] = self.typeChess
            self.rule.capture_stones(self.board,-self.typeChess)
        
    def ai_move(self):
        move = self.ai.get_next_move(self.board, -self.typeChess)
        # Đánh dấu nước đi của AI
        if move:
            x, y = move
            suicidal = self.rule.is_suicidal(self.board,x,y,-self.typeChess) 
            reapeated_state = self.rule.is_repeated_state(self.board,x,y,-self.typeChess)
            if suicidal and reapeated_state:
                self.current_turn = "Player"
                self.board[x][y] = -self.typeChess  
                self.rule.capture_stones(self.board,self.typeChess)
            return True
        elif move == None:
            self.current_turn = "Player"
            return False
        
    def test_ai_click(self, move):
        # Đánh dấu nước đi của AI
        if move:
            # Lấy tọa độ chuột
            mouse_x, mouse_y = move
            
            # Tính toán tọa độ ô gần nhất
            x = round((mouse_x - self.chessStart )/ self.spacing)  # Làm tròn tọa độ x
            y = round((mouse_y - self.chessStart) / self.spacing) # Làm tròn tọa độ y

            suicidal = self.rule.is_suicidal(self.board,x,y,-self.typeChess) 
            reapeated_state = self.rule.is_repeated_state(self.board,x,y,-self.typeChess)
            
            if suicidal and reapeated_state:
                self.current_turn = "Player"
                self.board[x][y] = -self.typeChess  
                self.rule.capture_stones(self.board,self.typeChess)

    def whoIsWinner(self):
        return self.rule.who_win(self.board)
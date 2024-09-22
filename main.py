import pygame
from board import Board
from ai import AI
from gameControl import GameControl

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cờ Vây AI")

# Font chữ
font = pygame.font.SysFont('Arial', 24)

#Khởi tạo thông số bàn cờ
'''
    19: (19,'19x19board.jpg', 31.3, 20, 12),
    sizeBoard: (sizeBoard, img, spacing, chessStart, chessSize)
    chessStart: là khoảng cách từ mép bàn cờ đến quân cờ cái này tự mò vì quân cờ bị chui vào bên trái mất tích
'''
choiceBoard = {
    19: (19,'19x19board.jpg', 31.3, 20, 12),
    13: (13,'13x13board.png', 45.5, 27, 17), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    9: (9,'9x9board.png', 66, 35, 22) # Các ae tự sửa chỗ này theo ảnh bàn cờ 
}

# Input đầu vào các options người dùng
# typeChess = int(input("Chọn quân cờ (1 - Trắng, -1 - Đen): "))
# sizeGame = int(input("Chọn kích thước bàn cờ (9, 13, 19): "))
typeChess = -1
sizeGame = 19

# Khởi tạo đối tượng
board = Board(choiceBoard[sizeGame],typeChess) 
gameControl = GameControl(screen, font, typeChess)
ai = AI()

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Xử lý sự kiện chuột cho nước đi của người chơi
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            board.player_move(pos)

    # Vẽ bàn cờ
    board.draw(screen)
    gameControl.draw_scoreboard(height)

    # AI đưa ra nước đi
    if board.current_turn == "AI":
        ai_move = ai.get_move(board)
        board.ai_move(ai_move)

    pygame.display.flip()

pygame.quit()

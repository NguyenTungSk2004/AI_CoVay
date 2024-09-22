import pygame
from board import Board
from ai import AI

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cờ Vây AI")


#Khởi tạo thông số bàn cờ


# Khởi tạo đối tượng Board và AI
board = Board(19,'19x19board.jpg',31.3,31.3,20) # 19x19 board with 31.3 spacing and 20 chessStart
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
    
    # AI đưa ra nước đi
    if board.current_turn == "AI":
        ai_move = ai.get_move(board)
        board.ai_move(ai_move)

    pygame.display.flip()

pygame.quit()

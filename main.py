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
'''
    19: (19,'19x19board.jpg', 31.3, 20, 12),
    sizeBoard: (sizeBoard, img, spacing, chessStart, chessSize)
    chessStart: là khoảng cách từ mép bàn cờ đến quân cờ cái này tự mò vì quân cờ bị chui vào bên trái mất tích
'''
choiceBoard = {
    19: (19,'19x19board.jpg', 31.3, 20, 12),
    13: (13,'13x13board.png', 45.5, 27, 17), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    9: (9,'9x9board.webp', 40, 145, 19) # Các ae tự sửa chỗ này theo ảnh bàn cờ 
}

# Khởi tạo đối tượng Board và AI
board = Board(choiceBoard[13]) 
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

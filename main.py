import pygame
from board import Board
from ai import AI
from gameControl import GameControl
import color

# Khởi tạo Pygame
pygame.init()

# Khởi tạo thông số cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cờ Vây AI")
font = pygame.font.SysFont('Arial', 24)

# #Khởi tạo thông số bàn cờ
# '''
#     19: (19,'19x19board.jpg', 31.3, 20, 12),
#     sizeBoard: (sizeBoard, img, spacing, chessStart, chessSize)
#     chessStart: là khoảng cách từ mép bàn cờ đến quân cờ cái này tự mò vì quân cờ bị chui vào bên trái mất tích
# '''
choiceBoard = {
    19: (19,'19x19board.jpg', 31.3, 20, 12),
    13: (13,'13x13board.png', 45.5, 27, 17), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    9: (9,'9x9board.png', 66, 35, 22) # Các ae tự sửa chỗ này theo ảnh bàn cờ 
}

# Khởi tạo cấu hình trò chơi
def initialize_game(screen, font, sizeGame, typeChess):
    player_name = "USER"
    board = Board(choiceBoard[sizeGame], typeChess)
    gameControl = GameControl(screen, font, typeChess, player_name, board)
    ai = AI()
    return board, gameControl, ai

# Input đầu vào các options người dùng
# typeChess = int(input("Chọn quân cờ (1 - Trắng, -1 - Đen): "))
# sizeGame = int(input("Chọn kích thước bàn cờ (9, 13, 19): "))
typeChess = -1
sizeGame = 19
board, gameControl, ai = initialize_game(screen, font, sizeGame, typeChess)

# Vòng lặp chính
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            # Xử lý sự kiện chuột cho nước đi của người chơi
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if gameControl.getSkipButton().collidepoint(pos):
                    # Người chơi nhấn nút "Bỏ qua"
                    board.current_turn = "AI"
                elif gameControl.surrender_button_rect.collidepoint(pos):
                    # Người chơi nhấn nút "Đầu hàng"
                    game_over = True
                else:
                    board.player_move(pos)
        else:
            exit_button_rect = gameControl.getExitButton()
            replay_button_rect = gameControl.getReplayButton()
            # Xử lý sự kiện chuột cho hộp thoại điểm
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(pos):
                    # Người chơi nhấn nút "Thoát"
                    running = False
                elif replay_button_rect.collidepoint(pos):
                    # Người chơi nhấn nút "Chơi lại"
                    game_over = False
                    board, gameControl, ai = initialize_game(screen, font, sizeGame, typeChess)

    # Vẽ bàn cờ
    board.draw(screen)
    gameControl.draw_scoreboard(height)
    if game_over:
        # Hiển thị hộp thoại điểm
        gameControl.draw_game_over_dialog() 

    # AI đưa ra nước đi
    if board.current_turn == "AI":
        ai_move = ai.get_move(board)
        board.ai_move(ai_move)

    pygame.display.flip()

pygame.quit()
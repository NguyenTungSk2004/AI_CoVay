import pygame
from board import Board
from gameControl import GameControl
from menu import Menu

from effect_game import start_game as Fighting
from setup import init_screen, load_font, load_background

# Khởi tạo Pygame
pygame.init()

# Khởi tạo thông số cửa sổ
width, height = 800, 600
screen = init_screen(width, height, "Game Cờ Vây")
font = load_font('tahoma', 30)
# Khởi tạo màn hình, phông chữ, hình nền và các biến
background_image = load_background('Nencv.jpg', width, height)

# Khởi tạo thông số bàn cờ
# '''
#     19: (19,'19x19board.jpg', 31.3, 20, 12),
#     sizeBoard: (sizeBoard, img, spacing, chessStart, chessSize)
#     chessStart: là khoảng cách từ mép bàn cờ đến quân cờ cái này tự mò vì quân cờ bị chui vào bên trái mất tích
# '''
choiceBoard = {
    "19x19": (19,'19x19board.jpg', 31.3, 20, 12),
    "13x13": (13,'13x13board.png', 45.5, 27, 17), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    "9x9": (9,'9x9board.png', 66, 35, 22), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    "7x7": (7,'7x7board.png', 83.5, 50, 30), # Các ae tự sửa chỗ này theo ảnh bàn cờ 
    "5x5": (5,'5x5board.png', 115, 70, 40) # Các ae tự sửa chỗ này theo ảnh bàn cờ 
}

# Khởi tạo cấu hình trò chơi
def initialize_game(screen, font, sizeGame, typeChess):
    typeChess = 1 if typeChess == "Trắng" else -1
    board = Board(choiceBoard[sizeGame], typeChess)
    gameControl = GameControl(screen, font, typeChess, player_name, board)
    return board, gameControl

# Khởi tạo các biến thông tin cơ bản
allChess = ["Đen", "Trắng"]
# board_sizes = ["5x5","7x7","9x9", "13x13", "19x19"]
board_sizes = ["5x5","7x7","9x9"]
player_name = ""
typeChess = None
sizeGame = None
input_active = False
play_active = False
board, gameControl = None, None

skipForGame = 0

init_variables =  [player_name, typeChess, sizeGame, input_active]
menu = Menu(screen, font, allChess, board_sizes, init_variables)

# Vòng lặp chính
running = True
game_over = False
while running:

    if play_active:
        #AI đưa ra nước đi
        if board.current_turn == "AI":
            check_ai_move = board.ai_move()
            if check_ai_move:
                gameControl.set_first_move_made()
                skipForGame = 0
                print(f"AI is ", board.whoIsWinner())

    input_box = menu.getInputBox()
    player_name = menu.getPlayerName()
    typeChess = menu.getSelectedChess()
    sizeGame = menu.getSelectedBoardSize()
    input_active = menu.getInputActive()
    
    if not play_active:
        # Vẽ Menu game
        screen.blit(background_image, (-20, 0))
        menu.draw_menu_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if play_active:
            if not game_over:
                # Xử lý sự kiện chuột cho nước đi của người chơi
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if gameControl.getSkipButton().collidepoint(pos):
                        # Người chơi nhấn nút "Bỏ qua"
                        skipForGame += 1 
                        if skipForGame == 2: game_over = True
                        board.current_turn = "AI" if board.current_turn == "Player" else "Player"

                    elif gameControl.surrender_button_rect.collidepoint(pos):
                        # Người chơi nhấn nút "Đầu hàng"
                        game_over = True
                    elif event.button == 1 and board.current_turn == "Player":
                        move_made = board.player_move(pos)
                        if move_made:  # Nếu đặt được quân cờ
                            gameControl.set_first_move_made()  # Đánh dấu đã có nước đi đầu tiên
                            print(f"Player is ", board.whoIsWinner())
                            skipForGame = 0
                        elif not board.has_valid_moves():
                            # Kiểm tra xem còn nước đi hợp lệ nào không
                            skipForGame += 1
                            if skipForGame == 2:
                                game_over = True
                            else:
                                board.current_turn = "AI"
                    # elif event.button == 3 and board.current_turn == "AI":
                    #     board.test_ai_click(pos)
                    #     skipForGame = 0
            else:
                # Xử lý sự kiện chuột cho hộp thoại kết thúc
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if gameControl.getExitButton().collidepoint(pos):
                        # Người chơi nhấn nút "Thoát"
                        play_active = False
                        game_over = False
                    elif gameControl.getReplayButton().collidepoint(pos):
                        # Người chơi nhấn nút "Chơi lại"
                        game_over = False
                        board, gameControl = initialize_game(screen, font, sizeGame, typeChess)
                        skipForGame = 0

        elif not play_active:
            # Menu game
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Xử lý click vào khung nhập tên người chơi
                if input_box.collidepoint(event.pos):
                    menu.setInputActive(True)
                else:
                    menu.setInputActive(False)
                # Xử lý lựa chọn loại quân
                for chess in allChess:
                    if menu.getAllChess(chess).collidepoint(event.pos):
                        menu.setSelectedChess(chess) 
                # Xử lý lựa chọn kích thước bàn cờ
                for size in board_sizes:
                    if menu.getBoardSizes(size).collidepoint(event.pos):
                        menu.setSelectedBoardSize(size)
                # Xử lý nút "Thoát"
                if menu.getExitButton().collidepoint(event.pos):
                    running = False
                # Xử lý nút "Chơi"
                if menu.getPlayButton().collidepoint(event.pos):
                    font = load_font('tahoma', 20)
                    Fighting(screen, width, height)
                    board, gameControl = initialize_game(screen, font, sizeGame, typeChess)
                    play_active = True
                    skipForGame = 0

            # Xử lý sự kiện nhập tên người chơi
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
                menu.setPlayerName(player_name)

    if play_active and board is not None:
        # Vẽ bàn cờ
        board.draw(screen)
        gameControl.draw_scoreboard(height)
        
        # Hiển thị hộp thoại điểm
        if game_over:
            gameControl.draw_game_over_dialog() 

    pygame.display.flip()

pygame.quit()
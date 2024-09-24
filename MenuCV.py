import pygame
import sys
from color import WHITE, BLACK, GRAY
from drawUI import Menu
from event_handler import handle_events
from setup import init_screen, load_font, load_background

pygame.init()

width = 800
height = 600
allChess = ["Đen", "Trắng"]
board_sizes = ["9x9", "13x13", "19x19"]

# Khởi tạo các biến thông tin cơ bản
player_name = " "
selected_chess = None
selected_board_size = None
input_active = False

# Khởi tạo màn hình, phông chữ, hình nền và các biến
screen = init_screen(width, height, "Menu Cờ Vây")
font = load_font('tahoma', 30)
background_image = load_background('Nencv.jpg', width, height)

init_variables =  [player_name, selected_chess, selected_board_size, input_active]
menu = Menu(screen, font, allChess, board_sizes, init_variables)

running = True
while running:
    screen.blit(background_image, (0, 0))

    input_box = menu.getInputBox()
    player_name = menu.getPlayerName()
    selected_chess = menu.getSelectedChess()
    selected_board_size = menu.getSelectedBoardSize()
    input_active = menu.getInputActive()


    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                menu.setInputActive(True)
            else:
                menu.setInputActive(False)

            for chess in allChess:
                if menu.getAllChess(chess).collidepoint(event.pos):
                    menu.setSelectedChess(chess) 

            for size in board_sizes:
                if menu.getBoardSizes(size).collidepoint(event.pos):
                    menu.setSelectedBoardSize(size)

            if menu.getExitButton().collidepoint(event.pos):
                pygame.quit()
                exit()

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode
            menu.setPlayerName(player_name)

    menu.draw_menu_game()
    pygame.display.flip()

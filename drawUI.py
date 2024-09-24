import pygame
import sys
import color
from setup import draw_text

class Menu:
    def __init__(self, screen, font, allChess, board_sizes,init_variables):
        self.screen = screen
        self.font = font 

        # Khởi tạo các hộp chứa thông tin, các nút bấm
        self.input_box = pygame.Rect(270, 100, 250, 40)
        self.exit_button = pygame.Rect(250, 320, 100, 50)
        BlackChess, WhiteChess = [pygame.Rect(270 + i * 150, 180, 100, 40) for i in range(2)]
        button_9x9, button_13x13, button_19x19 = [pygame.Rect(295 + i * 150, 250, 100, 40) for i in range(3)]

        self.allChess = {
            "Đen": BlackChess,
            "Trắng": WhiteChess
        }
        self.board_sizes = {
            "9x9": button_9x9,
            "13x13": button_13x13,
            "19x19": button_19x19
        }
        # Khởi tạo các biến nhận dữ liệu
        self.player_name = init_variables[0]
        self.selected_chess = init_variables[1]
        self.selected_board_size = init_variables[2]
        self.input_active = init_variables[3]

    # allChess
    def getAllChess(self,nameChess):
        return self.allChess[nameChess]
    
    # board_sizes
    def getBoardSizes(self, size):
        return self.board_sizes[size]
    
    # button thoát
    def getExitButton(self):
        return self.exit_button

    # input_box
    def getInputBox(self):
        return self.input_box

    # player_name
    def getPlayerName(self):
        return self.player_name
    def setPlayerName(self, player_name):
         self.player_name = player_name

    # selected_chess
    def getSelectedChess(self):
        return self.selected_chess
    def setSelectedChess(self, selected_chess):
        self.selected_chess = selected_chess

    # selected_board_size
    def getSelectedBoardSize(self):
        return self.selected_board_size
    def setSelectedBoardSize(self, selected_board_size):
        self.selected_board_size = selected_board_size

    # input_active
    def getInputActive(self):
        return self.input_active
    def setInputActive(self, input_active):
        self.input_active = input_active

    # Hàm vẽ hộp nhập liệu
    def draw_player_name_input(self, MyColor):
        pygame.draw.rect(self.screen, MyColor if self.input_active else color.WHITE, self.input_box, 2) # 2 là độ dày của box
        draw_text('Tên người chơi: ', self.font, MyColor, self.screen, 50, 100)
        draw_text(self.player_name, self.font, color.BLACK, self.screen, self.input_box.x + 5, self.input_box.y + 1)

    # Hàm vẽ lựa chọn loại quân
    def draw_color_selection(self):
        draw_text('Chọn loại quân:', self.font, color.WHITE, self.screen, 50, 180)
        for i, chess in enumerate(self.allChess):
            pygame.draw.rect(self.screen, color.GRAY if self.selected_chess == chess else color.WHITE, 
                         (270 + i * 150, 180, 100, 40))
            draw_text(chess, self.font, color.BLACK, self.screen, 280 + i * 150, 180)

    # Hàm vẽ lựa chọn kích thước bàn
    def draw_board_size_selection(self):
        draw_text('Chọn kích cỡ bàn:', self.font, color.WHITE, self.screen, 50, 250)
        for i, size in enumerate(self.board_sizes):
            pygame.draw.rect(self.screen, color.GRAY if self.selected_board_size == size else color.WHITE,
                         (295 + i * 150, 250, 100, 40))
            draw_text(size, self.font, color.BLACK, self.screen, 305 + i * 150, 250)
    # Hàm vẽ nút thoát
    def draw_exit_button(self):
        pygame.draw.rect(self.screen, color.WHITE, (250, 320, 100, 50))
        draw_text('Thoát', self.font, color.BLACK, self.screen, 258, 325)

    # Hàm vẽ menu game
    def draw_menu_game(self):
        draw_text('Cờ Vây - Menu', self.font, color.WHITE, self.screen, 250, 20)
        self.draw_player_name_input(color.WHITE)
        self.draw_color_selection()
        self.draw_board_size_selection()
        self.draw_exit_button()

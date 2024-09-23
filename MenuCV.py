import pygame
import sys

pygame.init()

# Kích thước màn hình
width, height = 750, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu Cờ Vây")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PURPLE = (193, 5, 198)

# Tải phông chữ hỗ trợ tiếng Việt (ví dụ như Arial hoặc Tahoma)
font = pygame.font.Font(pygame.font.match_font('tahoma'), 30)
# Biến lưu trữ thông tin
player_name = " "
selected_color = None
selected_board_size = None

# Các lựa chọn cho loại quân và kích thước bàn
colors = ["Đen", "Trắng"]
board_sizes = ["9x9", "13x13", "19x19"]

# Hộp nhập liệu tên người chơi
input_active = False
input_box = pygame.Rect(270, 130, 250, 40)

# Tải hình nền từ đường dẫn
background_image = pygame.image.load('Nencv.jpg')
background_image = pygame.transform.scale(background_image, (width, height))

# Hàm hiển thị văn bản
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    global input_active, player_name, selected_color, selected_board_size
    
    running = True
    while running:
        screen.blit(background_image, (0, 0))  
        
            # Vẽ tiêu đề
        draw_text('Cờ Vây - Menu', font, (240, 173, 78), screen, 250, 50)
        
        # Nhập tên người chơi
        draw_text('Tên người chơi: ', font, WHITE, screen, 50, 130)
        pygame.draw.rect(screen, GRAY if input_active else WHITE, input_box, 2)
        draw_text(player_name, font, BLACK, screen, input_box.x + 5, input_box.y + 1)
        
        # Chọn loại quân
        draw_text('Chọn loại quân:', font, WHITE, screen, 50, 210)
        for i, color in enumerate(colors):
            pygame.draw.rect(screen, GRAY if selected_color == color else WHITE, (270 + i * 150, 210, 100, 40))
            draw_text(color, font, BLACK, screen, 280 + i * 150, 210)
        
        # Chọn kích thước bàn
        draw_text('Chọn kích cỡ bàn:', font, WHITE, screen, 50, 280)
        for i, size in enumerate(board_sizes):
            pygame.draw.rect(screen, GRAY if selected_board_size == size else WHITE, (295 + i * 150, 280, 100, 40))
            draw_text(size, font, BLACK, screen, 305 + i * 150, 280)
        
        # Thoát
        pygame.draw.rect(screen, WHITE, (250, 350, 100, 50))
        draw_text('Thoát', font, BLACK, screen, 258, 355)
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                # Kiểm tra lựa chọn loại quân
                for i, color in enumerate(colors):
                    if pygame.Rect(270 + i * 150, 180, 100, 40).collidepoint(event.pos):
                        selected_color = color
                
                # Kiểm tra lựa chọn kích thước bàn
                for i, size in enumerate(board_sizes):
                    if pygame.Rect(295 + i * 150, 250, 100, 40).collidepoint(event.pos):
                        selected_board_size = size
                
                # Kiểm tra nút thoát
                if pygame.Rect(250, 320, 100, 50).collidepoint(event.pos):
                    running = False
            
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Xóa ký tự cuối
                else:
                    player_name += event.unicode  # Thêm ký tự vào tên

        pygame.display.flip()

main_menu()

pygame.quit()

import pygame

def init_screen(width, height, title="Menu Cờ Vây"):
    # Khởi tạo màn hình chính và tiêu đề
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen

def load_font(font_name='tahoma', size=30):
    # Tải phông chữ hỗ trợ tiếng Việt
    font = pygame.font.Font(pygame.font.match_font(font_name), size)
    return font

def load_background(image_path, width, height):
    # Tải và điều chỉnh kích thước hình nền
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (width+20, height))
    return background_image

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

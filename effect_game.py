import pygame
def start_game(screen, width, height):
    font = pygame.font.Font(None, 50)  
    message = "Fighting!"      
    text_color = (255, 255, 255)       
    box_color = (0, 0, 0)              

    # Vẽ hộp thông báo giữa màn hình
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))

    # Vẽ hộp thông báo
    box_rect = pygame.Rect(0, 0, text_rect.width + 20, text_rect.height + 20)
    box_rect.center = (width // 2, height // 2)

    screen.fill((255, 255, 255))  
    pygame.draw.rect(screen, box_color, box_rect)  
    screen.blit(text_surface, text_rect)  

    pygame.display.flip()  

    pygame.time.delay(2000)

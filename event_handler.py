import pygame

def handle_events(allChess, board_sizes,handle_variables):
    input_box = handle_variables[0]
    player_name = handle_variables[1]
    selected_chess = handle_variables[2]
    selected_board_size = handle_variables[3]
    input_active = handle_variables[4]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False

            for i, chess in enumerate(allChess):
                if pygame.Rect(270 + i * 150, 180, 100, 40).collidepoint(event.pos):
                    selected_chess = chess

            for i, size in enumerate(board_sizes):
                if pygame.Rect(295 + i * 150, 250, 100, 40).collidepoint(event.pos):
                    selected_board_size = size

            if pygame.Rect(250, 320, 100, 50).collidepoint(event.pos):
                return False, selected_chess, selected_board_size, input_active, player_name

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += event.unicode

    return selected_chess, selected_board_size, input_active, player_name

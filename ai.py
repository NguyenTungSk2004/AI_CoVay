from rules import Rules
class AI:
    def __init__(self):
        self.rule = Rules()

    def get_next_move(self, board_state, player):
        """
        Trả về nước đi tốt nhất cho người chơi dựa trên trạng thái bàn cờ hiện tại.
        
        :param board_state: Ma trận 2D đại diện cho trạng thái bàn cờ.
        :param player: Người chơi hiện tại (-1 là quân đen, 1 là quân trắng).
        :return: Tọa độ của nước đi tiếp theo (x, y).
        """
        best_move = None
        best_score = float('-inf') if player == -1 else float('inf')
        
        for move in self.get_valid_moves(board_state, player):
            new_board_state = self.simulate_move(board_state, move, player)
            score = self.minimax(new_board_state, depth=2, player=-player)
            if (player == -1 and score > best_score) or (player == 1 and score < best_score):
                best_score = score
                best_move = move
                
        return best_move

    def get_valid_moves(self, board_state, player):
        """
        Trả về danh sách các nước đi hợp lệ dựa trên trạng thái bàn cờ.
        (Hiện tại chỉ trả về các ô trống không bị chết.)
        
        :param board_state: Ma trận 2D đại diện cho trạng thái bàn cờ.
        :param player: Người chơi hiện tại (-1 là quân đen, 1 là quân trắng).
        :return: Danh sách các nước đi hợp lệ (x, y).
        """
        valid_moves = []
        map_check =[]
        size = len(board_state)

        for enemy_x in range(size):
            for enemy_y in range(size):
                if board_state[enemy_x][enemy_y] != 0:
                    map_check = map_check + self.rule.get_neighbors(enemy_x,enemy_y, board_state)

        for move_check in map_check:
            x,y = move_check
            suicidal = self.rule.is_suicidal(board_state, x, y,player)
            repeated_state = self.rule.is_repeated_state(board_state,x,y,player)
            if suicidal and repeated_state:
                valid_moves.append((x, y))
        return valid_moves

    def simulate_move(self, board_state, move, player):
        """
        Giả lập nước đi và trả về trạng thái bàn cờ mới.
        
        :param board_state: Ma trận 2D hiện tại.
        :param move: Tọa độ của nước đi (x, y).
        :param player: Người chơi thực hiện nước đi (-1 hoặc 1).
        :return: Trạng thái bàn cờ mới sau khi thực hiện nước đi.
        """
        new_board_state = [row[:] for row in board_state]
        x, y = move
        new_board_state[x][y] = player
        return new_board_state

    def minimax(self, board_state, depth, player):
        """
        Thuật toán Minimax để tìm nước đi tốt nhất.
        
        :param board_state: Ma trận 2D hiện tại.
        :param depth: Độ sâu tìm kiếm.
        :param player: Người chơi hiện tại (-1 hoặc 1).
        :return: Điểm số của trạng thái bàn cờ.
        """
        if depth == 0 or self.is_game_over(board_state):
            return self.evaluate_board(board_state, player)
        
        if player == -1:  # Max player
            max_eval = float('-inf')
            for move in self.get_valid_moves(board_state, player):
                new_board_state = self.simulate_move(board_state, move, player)
                eval = self.minimax(new_board_state, depth - 1, -player)
                max_eval = max(max_eval, eval)
            return max_eval
        else:  # Min player
            min_eval = float('inf')
            for move in self.get_valid_moves(board_state, player):
                new_board_state = self.simulate_move(board_state, move, player)
                eval = self.minimax(new_board_state, depth - 1, -player)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, board_state, player):
        """
        Hàm đánh giá trạng thái bàn cờ.
        Hiện tại chỉ đơn giản dựa trên số quân cờ của người chơi.
        
        :param board_state: Ma trận 2D hiện tại.
        :param player: Người chơi hiện tại (-1 hoặc 1).
        :return: Điểm số của trạng thái bàn cờ.
        """
        winner,white_score, black_score = self.rule.who_win(board_state) 
        return white_score if player == 1 else black_score

    def is_game_over(self, board_state):
        """
        Kiểm tra xem game có kết thúc hay không (ví dụ khi hết nước đi).
        
        :param board_state: Ma trận 2D hiện tại.
        :return: True nếu game kết thúc, ngược lại False.
        """
        return len(self.get_valid_moves(board_state, player=-1)) == 0 and len(self.get_valid_moves(board_state, player=1)) == 0


# board_size = 5  # Kích thước bàn cờ 5x5
# go_ai = AI(board_size)

# # Khởi tạo bàn cờ trống
# initial_board_state = [
#     [0, 1, 0, 0, 1],
#     [-1, 1, -1, 1, -1],
#     [1, 0, -1, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0]
# ]

# # Gọi hàm get_next_move để tìm nước đi tốt nhất cho quân đen (-1)
# best_move = go_ai.get_next_move(initial_board_state, player=-1)
# print(f"Nước đi tốt nhất cho quân đen (-1): {best_move}")
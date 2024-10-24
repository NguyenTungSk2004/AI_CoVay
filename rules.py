import numpy as np
class Rules:

    def __init__(self):
        # Trạng thái phụ thuộc của luật KO
        self.current_board = None  
        self.previous_board = None  
        
    def get_neighbors(self, row, col, board):
        """
            Trả về các ô lân cận (trên, dưới, trái, phải) của ô truyền vào.

            :param row: Chỉ số hàng của ô hiện tại.
            :param col: Chỉ số cột của ô hiện tại.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: Danh sách các ô lân cận hợp lệ (trong phạm vi bàn cờ).
        """
        board_size = len(board)
        neighbors = [
            (row-1, col),  # top
            (row+1, col),  # bottom
            (row, col-1),  # left
            (row, col+1)   # right
        ]
        # Lọc ra những ô lân cận hợp lệ
        return [(r, c) for r, c in neighbors if 0 <= r < board_size and 0 <= c < board_size]

    def is_captured(self, board, row, col):
        """
            Kiểm tra xem nhóm quân cờ tại vị trí (row, col) có bị bắt hay không.

            :param board: Ma trận 2D đại diện cho bàn cờ.
            :param row: Chỉ số hàng của ô hiện tại.
            :param col: Chỉ số cột của ô hiện tại.
            :return: Tuple (bool, set) - True nếu nhóm quân bị bắt, False nếu còn khí (ô trống).
                    Set chứa các ô thuộc nhóm quân đã kiểm tra.
        """
        color = board[row][col]
        visited = set()
        to_visit = [(row, col)]
        
        while to_visit:
            current = to_visit.pop()
            visited.add(current)
            
            for neighbor in self.get_neighbors(current[0], current[1], board):
                r, c = neighbor
                if board[r][c] == color and neighbor not in visited:
                    to_visit.append(neighbor)
                elif board[r][c] == 0:  # Nếu có khí (ô trống)
                    return False, visited  # Không bị bắt
        return True, visited  # Không còn khí, quân bị bắt


    def capture_stones(self, board, typeChess):
        """
            Thực hiện việc bắt quân cờ và trả về trạng thái bàn cờ sau khi bắt quân.

            :param board: Ma trận 2D đại diện cho trạng thái bàn cờ hiện tại.
            :param typeChess: Loại quân cờ cần kiểm tra và bắt (ví dụ: -1 là quân đen, 1 là quân trắng).
            :return: Ma trận 2D đại diện cho trạng thái bàn cờ sau khi bắt quân cờ.
        """
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == typeChess:  # Quân cần bắt
                    check, groupChess = self.is_captured(board, row, col)
                    if check:
                        for chess in groupChess:
                            board[chess[0]][chess[1]] = 0  # Loại bỏ quân bị bắt

    def is_suicidal(self, board_real, x, y, typeChess):
        """
            Kiểm tra xem nước đi (x, y) có tự tử hay khô.

            :param board: Ma trận 2D đại diện cho bàn cờ.
            :param row: Chỉ số hàng của nước đi.
            :param col: Chỉ số cột của nước đi.
            :param typeChess: Loại quân cờ cần kiểm tra (ví dụ: -1 là quân đen, 1 là quân trắng).
            :return: True nếu nước đi hợp lệ, ngược lại False.
        """

        board = [row[:] for row in board_real]
        size = len(board)
        if not (0 <= x < size and 0 <= y < size and board[x][y] == 0):
            return False
        board[x][y] = typeChess  
        self.capture_stones(board,-typeChess)
        not_alive, visited = self.is_captured(board, x, y)

        return not not_alive
    
    def check_duplicate(self, board_real):
        """
            Kiểm tra xem nước đi có bị trùng lặp hay không.

            Parameters:
            board_real (list): Bảng hiện tại của trò chơi.

            Returns:
            bool: Trả về True nếu nước đi hợp lệ, False nếu nước đi không hợp lệ.
        """
        # Tạo một bản sao của bảng hiện tại
        board = [row[:] for row in board_real]
        
        # Nếu đây là nước đi đầu tiên, lưu bảng hiện tại và trả về True
        if self.current_board is None:
            self.current_board = board
            return True
        
        # Nếu bảng hiện tại khác với bảng trước đó, cập nhật bảng trước đó và bảng hiện tại
        if board != self.previous_board: 
            self.previous_board = self.current_board
            self.current_board = board

        # Nếu bảng hiện tại giống với bảng trước đó, nước đi không hợp lệ
        if board == self.previous_board:
            return False

        # Nếu không có vấn đề gì, nước đi hợp lệ
        return True
    
    def is_repeated_state(self, board, x, y, typeChess):
        """
            Kiểm tra xem trạng thái của bảng có bị lặp lại hay không sau khi thực hiện một nước đi.

            Parameters:
            board (list): Bảng hiện tại của trò chơi.
            x (int): Chỉ số hàng của nước đi.
            y (int): Chỉ số cột của nước đi.
            typeChess (int): Loại quân cờ được đặt (ví dụ: 1 cho quân đen, -1 cho quân trắng).

            Returns:
            bool: Trả về True nếu trạng thái bảng bị lặp lại, False nếu không bị lặp lại.
        """
        # Tạo một bản sao của bảng hiện tại
        board = [row[:] for row in board]
        
        # Đặt quân cờ vào vị trí (x, y)
        board[x][y] = typeChess
        
        # Thực hiện bắt quân cờ của đối phương
        self.capture_stones(board, -typeChess)
        
        # Kiểm tra xem trạng thái bảng có bị lặp lại hay không
        return self.check_duplicate(board)

    def count_territory(self, board):
        """
            Đếm lãnh thổ của hai bên (trắng và đen) trên bàn cờ.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: Số lượng lãnh thổ của quân trắng và quân đen.
        """
        visited = np.zeros_like(board, dtype=bool)
        white_territory = black_territory = 0

        def is_surrounded(x, y):
            """
                Kiểm tra xem khu vực tại (x, y) có được bao quanh bởi quân trắng hoặc đen hay không.
                :param x: Chỉ số hàng của ô cần kiểm tra.
                :param y: Chỉ số cột của ô cần kiểm tra.
                :return: 1 nếu bao quanh bởi quân trắng, -1 nếu bao quanh bởi quân đen, 0 nếu không thuộc ai.
            """
            stack = [(x, y)]
            surrounded_by_black = surrounded_by_white = True
            territory_size = 0

            while stack:
                cx, cy = stack.pop()
                if visited[cx, cy]:
                    continue
                visited[cx, cy] = True
                territory_size += 1

                for nx, ny in self.get_neighbors(cx, cy, board):
                    if board[nx][ny] == 0 and not visited[nx, ny]:
                        stack.append((nx, ny))
                    elif board[nx][ny] == -1:
                        surrounded_by_white = False
                    elif board[nx][ny] == 1:
                        surrounded_by_black = False

            if surrounded_by_black and not surrounded_by_white:
                return -1, territory_size  # Bao quanh bởi quân đen
            elif surrounded_by_white and not surrounded_by_black:
                return 1, territory_size  # Bao quanh bởi quân trắng
            return 0, territory_size  # Không thuộc lãnh thổ ai

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0 and not visited[i, j]:
                    owner, territory_size = is_surrounded(i, j)
                    if owner == 1:
                        white_territory += territory_size
                    elif owner == -1:
                        black_territory += territory_size

        return white_territory, black_territory

    def count_stones(self, board):
        """
            Đếm số quân cờ trên bàn cờ của cả hai bên.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: Số lượng quân trắng và quân đen trên bàn cờ.
        """
        return np.sum(np.array(board) == 1), np.sum(np.array(board) == -1)

    def who_win(self, board):
        """
            Tính toán điểm của cả hai bên và xác định người chiến thắng.

            Parameters:
            board (list): Ma trận 2D đại diện cho bàn cờ.

            Returns:
            tuple: (1 nếu quân trắng thắng, -1 nếu quân đen thắng, điểm của quân trắng, điểm của quân đen)
        """
        white_territory, black_territory = self.count_territory(board)
        white_stones, black_stones = self.count_stones(board)
        white_score = white_stones + white_territory + 3.75  # Cộng thêm 3.75 điểm cho bên trắng
        black_score = black_stones + black_territory  # Điểm của quân đen
        
        return 1 if white_score > black_score else -1, white_score, black_score

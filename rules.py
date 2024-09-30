class Rules:
    """
        Code các luật ở đây
    """
    @classmethod
    def get_neighbors(cls, row, col, board):
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

    @classmethod
    def is_captured(cls, board, row, col):
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
            
            for neighbor in cls.get_neighbors(current[0], current[1], board):
                r, c = neighbor
                if board[r][c] == color and neighbor not in visited:
                    to_visit.append(neighbor)
                elif board[r][c] == 0:  # Nếu có khí (ô trống)
                    return False, visited  # Không bị bắt
        return True, visited  # Không còn khí, quân bị bắt


    @classmethod
    def capture_stones(cls, board, typeChess):
        """
        Thực hiện việc bắt quân cờ và trả về trạng thái bàn cờ sau khi bắt quân.

        :param board: Ma trận 2D đại diện cho trạng thái bàn cờ hiện tại.
        :param typeChess: Loại quân cờ cần kiểm tra và bắt (ví dụ: -1 là quân đen, 1 là quân trắng).
        :return: Ma trận 2D đại diện cho trạng thái bàn cờ sau khi bắt quân cờ.
        """
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == typeChess:  # Quân cần bắt
                    check, groupChess = cls.is_captured(board, row, col)
                    if check:
                        for chess in groupChess:
                            board[chess[0]][chess[1]] = 0  # Loại bỏ quân bị bắt

    @classmethod
    def is_valid_move(cls, board_real, x, y, typeChess):
        """
        Kiểm tra xem nước đi (x, y) có hợp lệ không.

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
        Rules.capture_stones(board,-typeChess)
        not_alive, visited = Rules.is_captured(board, x, y)

        return not not_alive
    
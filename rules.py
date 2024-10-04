import numpy as np
import tkinter as tk
from tkinter import messagebox
import board

class Rules:
    """
        Các luật của Cờ Vây.
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
        return [(r, c) for r, c in neighbors if 0 <= r < board_size and 0 <= c < board_size]

    @classmethod
    def is_captured(cls, board, row, col):
        """ Kiểm tra xem nhóm quân cờ tại vị trí (row, col) có bị bắt hay không.
        :param board: Ma trận 2D đại diện cho bàn cờ.
        :param row: Chỉ số hàng của ô hiện tại.
        :param col: Chỉ số cột của ô hiện tại.
        :return: Tuple (bool, set) - True nếu nhóm quân bị bắt, False nếu còn khí (ô trống).
            Set chứa các ô thuộc nhóm quân đã kiểm tra."""
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
                elif board[r][c] == 0:
                    return False, visited  # Không bị bắt
        return True, visited  # Quân bị bắt

    @classmethod
    def capture_stones(cls, board, typeChess):
        """
            Kiểm tra và loại bỏ các nhóm quân bị bắt trên bàn cờ.
            :param board: Ma trận 2D đại diện cho bàn cờ, chứa các giá trị đại diện cho quân cờ (1 cho trắng, -1 cho đen, 0 cho ô trống).
            :param typeChess: Loại quân cờ cần kiểm tra (1 cho trắng, -1 cho đen).
            :return: Ma trận bàn cờ sau khi loại bỏ các quân cờ bị bắt.
        """
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == typeChess:
                    check, groupChess = cls.is_captured(board, row, col)
                    if check:
                        for chess in groupChess:
                            board[chess[0]][chess[1]] = 0  # Loại bỏ quân bị bắt
        return board
    def is_valid_move(cls, board_real, x, y, typeChess):
        """
            Kiểm tra xem nước đi tại vị trí (x, y) có hợp lệ không.
            :param board_real: Ma trận 2D đại diện cho bàn cờ hiện tại.
            :param x: Chỉ số hàng của vị trí đặt quân.
            :param y: Chỉ số cột của vị trí đặt quân.
            :param typeChess: Loại quân cờ muốn đặt (1 cho quân trắng, -1 cho quân đen).
            :return: Trả về True nếu nước đi hợp lệ, ngược lại trả về False.
        """
        board = [row[:] for row in board_real]  # Tạo bản sao của board
        size = len(board)
        if not (0 <= x < size and 0 <= y < size and board[x][y] == 0):
            return False
        board[x][y] = typeChess  # Đặt quân cờ
        cls.capture_stones(board, -typeChess)  # Bắt quân đối phương
        not_alive, _ = cls.is_captured(board, x, y)  # Kiểm tra nếu nước đi này không hợp lệ (tự sát)
        return not not_alive

    @classmethod
    def count_territory(cls, board):
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

                for nx, ny in cls.get_neighbors(cx, cy, board):
                    if board[nx][ny] == 0 and not visited[nx, ny]:
                        stack.append((nx, ny))
                    elif board[nx][ny] == 1:
                        surrounded_by_white = False
                    elif board[nx][ny] == -1:
                        surrounded_by_black = False

            if surrounded_by_black and not surrounded_by_white:
                return 1, territory_size  # Bao quanh bởi quân trắng
            elif surrounded_by_white and not surrounded_by_black:
                return -1, territory_size  # Bao quanh bởi quân đen
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

    @classmethod
    def count_stones(cls, board):
        """
            Đếm số quân cờ trên bàn cờ của cả hai bên.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: Số lượng quân trắng và quân đen trên bàn cờ.
        """
        return np.sum(np.array(board) == 1), np.sum(np.array(board) == -1)

    @classmethod
    def evaluate(cls, board):
        """
            Tính toán điểm của cả hai bên và xác định người chiến thắng.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: True nếu quân trắng thắng, False nếu quân đen thắng.
        """
        white_territory, black_territory = cls.count_territory(board)
        white_stones, black_stones = cls.count_stones(board)
        white_score = white_stones + white_territory + 3.75  # Cộng thêm 3.75 điểm cho bên trắng
        black_score = black_stones + black_territory  # Điểm của quân đen

        print(f"Số quân trắng còn lại: {white_stones}")
        print(f"Số quân đen còn lại: {black_stones}")
        print(f"Lãnh thổ quân trắng: {white_territory}")
        print(f"Lãnh thổ quân đen: {black_territory}")
        print(f"Điểm của quân trắng (bao gồm cộng điểm): {white_score}")
        print(f"Điểm của quân đen (bao gồm cộng điểm): {black_score}")

        result_text = (f"Quân trắng thắng với {white_score} điểm!" if white_score > black_score 
                       else f"Quân đen thắng với {black_score} điểm!")
        
        # Hiển thị kết quả trong hộp thoại
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính
        messagebox.showinfo("Kết quả", result_text)

        return white_score > black_score  # Trả về True nếu trắng thắng, False nếu đen thắng




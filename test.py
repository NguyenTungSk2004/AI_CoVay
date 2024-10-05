import numpy as np

class Rules:
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
        return [(r, c) for r, c in neighbors if 0 <= r < board_size and 0 <= c < board_size]

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

    def count_stones(self, board):
        """
            Đếm số quân cờ trên bàn cờ của cả hai bên.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: Số lượng quân trắng và quân đen trên bàn cờ.
        """
        return np.sum(np.array(board) == 1), np.sum(np.array(board) == -1)

    def evaluate(self, board):
        """
            Tính toán điểm của cả hai bên và xác định người chiến thắng.
            :param board: Ma trận 2D đại diện cho bàn cờ.
            :return: True nếu quân trắng thắng, False nếu quân đen thắng.
        """
        white_territory, black_territory = self.count_territory(board)
        white_stones, black_stones = self.count_stones(board)
        white_score = white_stones + white_territory + 3.75  # Cộng thêm 3.75 điểm cho bên trắng
        black_score = black_stones + black_territory  # Điểm của quân đen

        print(f"Số quân trắng còn lại: {white_stones}")
        print(f"Số quân đen còn lại: {black_stones}")
        print(f"Lãnh thổ quân trắng: {white_territory}")
        print(f"Lãnh thổ quân đen: {black_territory}")
        print(f"Điểm của quân trắng (bao gồm cộng điểm): {white_score}")
        print(f"Điểm của quân đen (bao gồm cộng điểm): {black_score}")
        return white_score > black_score  # Trả về True nếu trắng thắng, False nếu đen thắng


# Bảng cờ mẫu (9x9)
test = [
    [ 0, 0,-1,0,0,0,0],
    [1, 1,-1,0,1,1,1],
    [ 1, 0,-1,0,1,0,0],
    [-1,-1, -1,0,1,1,1],
    [ 0, 0, -1,0,0,0,0],
    [ 0, 0, -1,0,0,0,0],
    [ 0, 0, -1,0,0,0,0],
]


game = Rules()
game.evaluate(test)
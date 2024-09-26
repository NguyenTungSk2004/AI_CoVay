"""
    Code các luật ở đây
"""
class Rules:
    """
        output: các ô bên trên, dưới, trái phải của ô truyền vào
    """
    @classmethod
    def get_neighbors(cls, row, col, board):
        board_size = len(board)
        neighbors = [
            (row-1, col),  # top
            (row+1, col),  # bottom
            (row, col-1),  # left
            (row, col+1)   # right
        ]
        # Lọc ra những ô lân cận hợp lệ
        return [(r, c) for r, c in neighbors if 0 <= r < board_size and 0 <= c < board_size]

    """
        output: kiểm tra xem nhóm quân cờ còn khí hay không.
    """
    @classmethod
    def is_captured(cls, board, row, col):
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

    """
        output: bàn cờ sau khi bắt quân cờ
    """
    @classmethod
    def capture_stones(cls, board, typeChess):
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == typeChess:  # Quân hiện tại
                    check, groupChess = cls.is_captured(board, row, col)
                    if check:
                        for chess in groupChess:
                            board[chess[0]][chess[1]] = 0  # Loại bỏ quân bị bắt
        return board
    

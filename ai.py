class AI:
    def get_move(self, board):
        # Giả lập nước đi AI, có thể phát triển thêm thuật toán Minimax
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] == 0:
                    return (x, y)  # Chọn ô trống đầu tiên
        return None

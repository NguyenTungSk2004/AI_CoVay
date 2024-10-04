from rules import Rules
class KO_rule:
    def __init__(self):
        self.current_board = None  
        self.previous_board = None  

    def check_duplicate(self, board_real):
        board = [row[:] for row in board_real]
        
        if self.current_board is None:
            self.current_board = board
            print("Nuoc dau tien")
            return True
        
        if board != self.previous_board: 
            self.previous_board = self.current_board
            self.current_board = board

        if board == self.previous_board:
            print("Nuoc di khong hop le")
            return False

        print("Nuoc di hop le")
        return True
    def is_repeated_state(self,board,x,y,typeChess):
        #tạo cái board với nước đi là (x,y) ở đây
        board = [row[:] for row in board]
        board[x][y] = typeChess
        Rules.capture_stones(board,-typeChess)
        return self.check_duplicate(board)

# game = KO_rule()


# test1 = [
#     [0, 0, 0, 0, 0],
#     [0, 1, -1, 0, 0],
#     [1, 0, 1, -1, 0],
#     [0, 1, -1, 0, 0],
#     [0, 0, 0, 0, 0],
# ]

# test2 = [
#     [0, 0, 0, 0, 0],
#     [0, 1, -1, 0, 0],
#     [1, -1, 0, -1, 0],
#     [0, 1, -1, 0, 0],
#     [0, 0, 0, 0, 0],
# ]

# game.check_duplicate(test1) #ng
# game.check_duplicate(test2) #ai
# game.is_repeated_state(test2,2,2,1) #ng
# for row in test2:
#     print(row)
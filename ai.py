import random
from rules import Rules
class AI:
    def __init__(self):
        self.rule = Rules()

    def get_next_move(self, boardState, AI):
        """
        Trả về nước đi tốt nhất cho người chơi dựa trên trạng thái bàn cờ hiện tại.
        
        :param boardState: Ma trận 2D đại diện cho trạng thái bàn cờ.
        :param AI: Người chơi hiện tại (-1 là quân đen, 1 là quân trắng).
        :return: Tọa độ của nước đi tiếp theo (x, y).
        """
        def get_best_move(score, bestScore):
            if (AI == -1 and score < bestScore) or (AI == 1 and score > bestScore):
                bestScore = score
            return bestScore


        bestMove = []
        bestScore = float('inf') if AI == -1 else -float('inf')
        mapMove = {}
        validMoves = self.get_valid_moves(boardState, AI)

        if self.ai_skip(boardState, validMoves, AI): return None 

        for move in validMoves:
            newBoardState = self.simulate_move(boardState, move, AI)
            currentScore = self.evaluate_board(newBoardState)
            score, board = self.minimax(newBoardState, currentScore, depth=2, AI=-AI)
            bestScore = get_best_move(score, bestScore)

            mapMove[move] = score

        for move in mapMove:
            if mapMove[move] == bestScore:
                bestMove.append(move)

        result = None
        if bestMove:
            result = random.choice(bestMove) 
        return result

    def get_valid_moves(self, boardState, AI):
        """
        Trả về danh sách các nước đi hợp lệ dựa trên trạng thái bàn cờ.
        (Hiện tại chỉ trả về các ô trống không bị chết.)
        
        :param boardState: Ma trận 2D đại diện cho trạng thái bàn cờ.
        :param AI: Người chơi hiện tại (-1 là quân đen, 1 là quân trắng).
        :return: Danh sách các nước đi hợp lệ (x, y).
        """
        validMoves = []
        size = len(boardState)

        for x in range(size):
            for y in range(size):
                if boardState[x][y] == 0:
                    suicidal = self.rule.is_suicidal(boardState, x, y,AI)
                    repeatedState = self.rule.is_repeated_state(boardState,x,y,AI)
                    if suicidal and repeatedState:
                        validMoves.append((x, y))
        return validMoves

    def simulate_move(self, boardState, move, AI):
        """
        Giả lập nước đi và trả về trạng thái bàn cờ mới.
        
        :param boardState: Ma trận 2D hiện tại.
        :param move: Tọa độ của nước đi (x, y).
        :param AI: Người chơi thực hiện nước đi (-1 hoặc 1).
        :return: Trạng thái bàn cờ mới sau khi thực hiện nước đi.
        """
        newBoardState = [row[:] for row in boardState]
        x, y = move
        newBoardState[x][y] = AI
        self.rule.capture_stones(newBoardState, -AI)
        return newBoardState

    def minimax(self, boardState, currentScore, depth, AI):
        """
        Thuật toán Minimax để tìm nước đi tốt nhất (sử dụng vòng lặp thay vì đệ quy).
        
        :param boardState: Ma trận 2D hiện tại.
        :param depth: Độ sâu tìm kiếm.
        :param AI: Người chơi hiện tại (-1 hoặc 1).
        :return: Điểm số của trạng thái bàn cờ.
        """
        stack = [(boardState, depth, AI)]
        bestScore = currentScore
        board = boardState
        while stack:
            currentBoard, currentDepth, currentAI = stack.pop()

            if currentDepth == 0:
                score = self.evaluate_board(currentBoard)
                bestScore = max(bestScore, score) if AI == 1 else min(bestScore, score)
                board = currentBoard
                continue

            if currentAI == 1:  # Max AI
                maxEval = bestScore
                for move in self.get_valid_moves(currentBoard, currentAI):
                    newBoardState = self.simulate_move(currentBoard, move, currentAI)
                    stack.append((newBoardState, currentDepth - 1, -currentAI))
                    maxEval = max(maxEval, bestScore)
                bestScore = max(bestScore, maxEval)
            else:  # Min AI
                minEval = bestScore
                for move in self.get_valid_moves(currentBoard, currentAI):
                    newBoardState = self.simulate_move(currentBoard, move, currentAI)
                    stack.append((newBoardState, currentDepth - 1, -currentAI))
                    minEval = min(minEval, bestScore)
                bestScore = min(bestScore, minEval)
        return bestScore, board

    def evaluate_board(self, boardState):
        """
        Hàm đánh giá trạng thái bàn cờ.
        Hiện tại chỉ đơn giản dựa trên số quân cờ của người chơi.
        
        :param boardState: Ma trận 2D hiện tại.
        :return: Điểm số của trạng thái bàn cờ.
        """
        whiteScore, blackScore = self.rule.who_win(boardState) 
        return whiteScore-blackScore
    
    def ai_skip(self, boardState, validMoves, AI):
        whiteStones, blackStones = self.rule.count_stones(boardState)
        currentStones = whiteStones if AI == 1 else blackStones
        currentScore = self.evaluate_board(boardState)

        for move in validMoves:
            newBoardState = self.simulate_move(boardState, move, AI)
            white, black = self.rule.count_stones(newBoardState)
            newStones = white if AI == 1 else black
            newScore = self.evaluate_board(newBoardState)

            if not (newStones > currentStones and newScore > currentScore) and AI == 1:
                return False
            if not (newStones > currentStones and newScore < currentScore) and AI == -1:
                return False
        return True


# import time 
# board_size = 5  # Kích thước bàn cờ 5x5
# go_ai = AI()

# # initial_boardState = [
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [-1, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, -1, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 1, -1, 1, 0, 0, 0, 0, 0],
# # ]

# # initial_boardState = [
# #     [0, 1, -1, 1, 0, 0, 0, 0, 0],
# #     [0, -1, 0, 0, 0, 0, 0, 0, 0],
# #     [-1, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [-1, 0, 0, 0, 0, 0, 0, 0, 0],
# #     [0, -1, 0, 0, 0, 0, 0, 0, 0],
# #     [0, 1, -1, 1, 0, 0, 0, 0, 0],
# # ]

# # initial_boardState = [
# #     [1,  1,  1,  0,  1],
# #     [1, -1, -1,  1,  -1],
# #     [1,  0, -1, -1,  0],
# #     [-1,-1,  0, -1, -1],
# #     [0,  1,  1, -1,  0],
# # ]

# initial_boardState = [
#     [-1,-1,  0,-1,  1],
#     [1,  1, -1, 0,  1],
#     [1, -1, -1, 0,  1],
#     [1, -1, -1,-1, -1],
#     [0, -1,  1, 1,  0],
# ]

# AI = 1
# start_time = time.time()
# best_move = go_ai.get_next_move(initial_boardState, AI)
# end_time = time.time()
# print("Thời gian tính toán:", end_time - start_time)
# print(f"Nước đi tốt nhất cho quân {AI}: {best_move}")
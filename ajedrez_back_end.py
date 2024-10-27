import math

class ChessPiece:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        raise NotImplementedError("This method should be overridden by subclasses")

    def evaluate(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class King(ChessPiece):
    def valid_moves(self, position, board):
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx != 0 or dy != 0):  # Ignorar la posición actual
                    new_x, new_y = position[0] + dx, position[1] + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_piece = board[new_x][new_y]
                        if target_piece is None or target_piece.color != self.color:
                            moves.append((new_x, new_y))
        return moves

    def evaluate(self):
        return 0  # No valor


class Queen(ChessPiece):
    def valid_moves(self, position, board):
        return self._linear_moves(position, board)

    def _linear_moves(self, position, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            x, y = position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                target_piece = board[x][y]
                if target_piece is None:
                    moves.append((x, y))
                elif target_piece.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

    def evaluate(self):
        return 9


class Rook(ChessPiece):
    def valid_moves(self, position, board):
        return self._linear_moves(position, board)

    def _linear_moves(self, position, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x, y = position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                target_piece = board[x][y]
                if target_piece is None:
                    moves.append((x, y))
                elif target_piece.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

    def evaluate(self):
        return 5


class Bishop(ChessPiece):
    def valid_moves(self, position, board):
        return self._linear_moves(position, board)

    def _linear_moves(self, position, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            x, y = position
            while True:
                x += dx
                y += dy
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                target_piece = board[x][y]
                if target_piece is None:
                    moves.append((x, y))
                elif target_piece.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

    def evaluate(self):
        return 3


class Knight(ChessPiece):
    def valid_moves(self, position, board):
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in offsets:
            new_x, new_y = position[0] + dx, position[1] + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target_piece = board[new_x][new_y]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((new_x, new_y))
        return moves

    def evaluate(self):
        return 3


class Pawn(ChessPiece):
    def valid_moves(self, position, board):
        moves = []
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6

        # Mover hacia adelante
        if self.can_move_forward(position, board, direction):
            moves.append((position[0] + direction, position[1]))
            if position[0] == start_row and self.can_move_forward((position[0] + direction, position[1]), board, direction):
                moves.append((position[0] + 2 * direction, position[1]))

        # Capturas diagonales
        self.check_diagonal_captures(position, moves, board, direction)
        return moves

    def can_move_forward(self, position, board, direction):
        return 0 <= position[0] + direction < 8 and board[position[0] + direction][position[1]] is None

    def check_diagonal_captures(self, position, moves, board, direction):
        for dy in [-1, 1]:
            new_x, new_y = position[0] + direction, position[1] + dy
            if 0 <= new_y < 8:
                target_piece = board[new_x][new_y]
                if target_piece and target_piece.color != self.color:
                    moves.append((new_x, new_y))

    def evaluate(self):
        return 1


class Board:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 'white'  # 'white' o 'black'

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        # Inicializar piezas para el jugador blanco
        board[0] = [
            Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
            King('white'), Bishop('white'), Knight('white'), Rook('white')
        ]
        board[1] = [Pawn('white') for _ in range(8)]

        # Inicializar piezas para el jugador negro
        board[7] = [
            Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
            King('black'), Bishop('black'), Knight('black'), Rook('black')
        ]
        board[6] = [Pawn('black') for _ in range(8)]

        return board

    def display_board(self):
        for row in self.board:
            print(" | ".join(["." if piece is None else piece.color[0] for piece in row]))
        print("\n")

    def is_valid_move(self, start, end):
        piece = self.board[start[0]][start[1]]
        if piece is None or (piece.color == 'white' and self.board[end[0]][end[1]] and self.board[end[0]][end[1]].color == 'white') or (piece.color == 'black' and self.board[end[0]][end[1]] and self.board[end[0]][end[1]].color == 'black'):
            return False
        return end in piece.valid_moves(start, self.board)

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False

    def evaluate_board(self):
        total_score = 0
        for row in self.board:
            for piece in row:
                if piece is not None:
                    score = piece.evaluate()
                    total_score += score if piece.color == 'white' else -score
        return total_score


class ChessAI:
    def __init__(self, depth):
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return board.evaluate_board()

        legal_moves = [(i, j) for i in range(8) for j in range(8) if board.is_valid_move((i, j), (ni, nj))]

        if maximizing_player:
            max_eval = -math.inf
            for start in legal_moves:
                for end in board.board[start[0]][start[1]].valid_moves(start, board):
                    board.move_piece(start, end)
                    eval = self.minimax(board, depth - 1, alpha, beta, False)
                    board.move_piece(end, start)  # Undo move
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for start in legal_moves:
                for end in board.board[start[0]][start[1]].valid_moves(start, board):
                    board.move_piece(start, end)
                    eval = self.minimax(board, depth - 1, alpha, beta, True)
                    board.move_piece(end, start)  # Undo move
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def best_move(self, board):
        best_eval = -math.inf
        best_move = None
        legal_moves = [(i, j) for i in range(8) for j in range(8) if board.is_valid_move((i, j), (ni, nj))]
        
        for start in legal_moves:
            for end in board.board[start[0]][start[1]].valid_moves(start, board):
                board.move_piece(start, end)
                eval = self.minimax(board, self.depth - 1, -math.inf, math.inf, False)
                board.move_piece(end, start)  # Undo move
                if eval > best_eval:
                    best_eval = eval
                    best_move = (start, end)
        
        return best_move


def main():
    game_board = Board()
    ai = ChessAI(depth=3)
    
    while True:
        game_board.display_board()
        if game_board.current_player == 'white':
            start = tuple(map(int, input("Enter the start position (row col): ").split()))
            end = tuple(map(int, input("Enter the end position (row col): ").split()))
            if not game_board.move_piece(start, end):
                print("Invalid move. Try again.")
        else:
            print("AI is making a move...")
            move = ai.best_move(game_board)
            if move:
                game_board.move_piece(move[0], move[1])
            else:
                print("No valid moves available for AI.")

if __name__ == "__main__":
    main()

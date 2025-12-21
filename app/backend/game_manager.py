import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.players = []
        self.current_turn = 0  # 0 for white, 1 for black
        self.time = {0: 60, 1: 60}  # 1 minute each
        self.move_history = {0: [], 1: []}
        self.game_over = False
        self.winner = None
    
    def make_move(self, player_id, move_uci):
        if self.game_over:
            return "Game is already over."
        if player_id != self.current_turn:
            return "It's not your turn."
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history[player_id].append(move_uci)
                self.current_turn = 1 - self.current_turn  # Switch turns
                if self.board.is_game_over():
                    self.game_over = True
                    result = self.board.result()
                    if result == '1-0':
                        self.winner = 0
                    elif result == '0-1':
                        self.winner = 1
                    else:
                        self.winner = None
                return "Move accepted."
            else:
                return "Illegal move."
        except ValueError:
            return "Invalid move format."

        
    def add_player(self, player_id):
        if len(self.players) < 2:
            self.players.append(player_id)
            return "Player added."
        else:
            return "Game already has two players."

    def get_game_state(self):
        return {
            "board_fen": self.board.fen(),
            "current_turn": self.current_turn,
            "time": self.time,
            "move_history": self.move_history,
            "game_over": self.game_over,
            "winner": self.winner
        }

    def display_board(self):
        print(self.board)

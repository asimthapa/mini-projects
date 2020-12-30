import random


class TicTacToe:
    def __init__(self, player1, player2, board=None):
        if board is None:
            self.board = [['.', '.', '.'],
                          ['.', '.', '.'],
                          ['.', '.', '.']]
        else:
            self.board = board

        self.player1 = player1
        self.player2 = player2
        self.winner = None

    def play(self, draw_board=False):
        current_player = self.player1
        next_player = self.player2

        while True:
            if draw_board:
                self.draw_board()
            if current_player[0] == 'user':
                self.human_move(current_player[1])
            else:
                if current_player[0] == 'easy':
                    print('Making move level "easy"')
                    self.easy_ai_move(current_player[1])
                elif current_player[0] == 'medium':
                    print('Making move level "medium"')
                    self.medium_ai_move(current_player[1], next_player[1])
                elif current_player[0] == 'hard':
                    print('Making move level "hard"')
                    self.hard_ai_move(current_player[1], next_player[1])

            # Check if game ended
            self.winner = self.is_over()
            if self.winner:
                if draw_board:
                    self.draw_board()
                return self.winner

            # Change turn
            next_player = current_player
            current_player = self.player1 if current_player == self.player2 else self.player2

    def human_move(self, player_piece):
        while True:
            user_input = input("Enter the coordinates: ")
            try:
                row, col = user_input.split()
                row, col = int(row)-1, int(col)-1
            except ValueError:
                print("You should enter numbers!")
                continue

            if row > 2 or row < 0 or col > 2 or col < 0:
                print("Coordinates should be from 1 to 3!")
                continue
            if self.board[row][col] != '.':
                print("This cell is occupied! Choose another one!")
                continue

            self.board[row][col] = player_piece
            return

    def easy_ai_move(self, player_piece):
        while True:
            row, col = random.choice([0, 1, 2]), random.choice([0, 1, 2])
            if self.board[row][col] == '.':
                self.board[row][col] = player_piece
                return

    def medium_ai_move(self, player_piece, opponent_piece):
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '.':
                    self.board[row][col] = player_piece
                    if self.is_over() == player_piece:
                        return
                    self.board[row][col] = opponent_piece
                    if self.is_over() == opponent_piece:
                        best_move = [row, col]
                    self.board[row][col] = '.'
        if best_move is None:
            self.easy_ai_move(player_piece)
        else:
            self.board[best_move[0]][best_move[1]] = player_piece

    def hard_ai_move(self, player_piece, opponent_piece):
        _, row, col = self.minimax(player_piece, opponent_piece, -100, 100, True)
        self.board[row][col] = player_piece
        return

    def draw_board(self):
        print("---------")
        for row_i in range(len(self.board)):
            for column_count, val in enumerate(self.board[row_i]):
                if column_count == 0:
                    print("|", end="")
                if val == ".":
                    print("".rjust(2), end="")
                else:
                    print(f"{val}".rjust(2), end="")

                if column_count == 2:
                    print(" |")
        print("---------")

    def is_over(self):
        # Horizontal win
        for i in range(3):
            if self.board[i] == ['X', 'X', 'X']:
                return 'X'
            elif self.board[i] == ['O', 'O', 'O']:
                return 'O'

        # Vertical win
        for i in range(3):
            if self.board[0][i] != '.' and self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i]:
                return self.board[0][i]

        # Main diagonal win
        if self.board[0][0] != '.' and self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            return self.board[0][0]

        # Second diagonal win
        if self.board[0][2] != '.' and self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            return self.board[0][2]

        # Is whole board full ?
        for i in range(3):
            for j in range(3):
                # Board is not full, continue playing
                if self.board[i][j] == '.':
                    return None

        # Board is indeed full and it's a tie
        return '.'

    def minimax(self, player_piece, opponent_piece, alpha, beta, is_max=True):
        result = self.is_over()

        if result == player_piece:
            return 1, 0, 0
        elif result == opponent_piece:
            return -1, 0, 0
        elif result == ".":
            return 0, 0, 0

        if is_max:
            max_val = -100
            max_row = max_col = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] != '.':
                        continue
                    self.board[i][j] = player_piece
                    evaluation, _, _ = self.minimax(player_piece, opponent_piece, alpha, beta, False)
                    # Reset the position
                    self.board[i][j] = '.'

                    if evaluation > max_val:
                        max_val, max_row, max_col = evaluation, i, j
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        return max_val, max_row, max_col
            return max_val, max_row, max_col
        else:
            min_val = 100
            min_row = min_col = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] != '.':
                        continue
                    self.board[i][j] = opponent_piece
                    evaluation, _, _ = self.minimax(player_piece, opponent_piece, alpha, beta, True)
                    # Reset the position
                    self.board[i][j] = '.'

                    if evaluation < min_val:
                        min_val, min_row, min_col = evaluation, i, j
                    beta = min(evaluation, beta)
                    if beta <= alpha:
                        return min_val, min_row, min_col
            return min_val, min_row, min_col


def main():
    legit_players = {'user', 'easy', 'medium', 'hard'}
    while True:
        commands = input("Input command: ")
        commands = commands.split()
        if commands[0] == "exit":
            return
        if commands[0] != "start" or len(commands) != 3 or commands[1] not in legit_players or commands[2] not in legit_players:
            print("Bad parameters!")
            continue

        player1 = (commands[1], 'X')
        player2 = (commands[2], 'O')

        game = TicTacToe(player1, player2)
        winner = game.play(draw_board=True)
        if winner == '.':
            print("Draw")
        else:
            print(f"{winner} wins")


main()

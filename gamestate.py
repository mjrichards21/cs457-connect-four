class Player:
    def _init_(self):
        self.token = "O"
        self.addr = None
        self.turn = False

class Game:
    def __init__(self):
        self.num_players = 0
        self.max_players = 2
        self.board_size = 7
        self.players = []
        self.player_turn = 0
        self.code = 1234
        self.num_spaces = 42
        self.turns_played = 0
        self.board = [[" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "]]
        
    def start_game(self, clients):
        print("Game started!")
        self.players = []
        self.board = [[" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "]]
        player_one = Player()
        player_one.addr = clients[0][1]
        player_one.token = "O"
        player_one.turn = True
        self.players.append(player_one)
        player_two = Player()
        player_two.addr = clients[1][1]
        player_two.token = "X"
        player_two.turn = False
        self.players.append(player_two)
        self.turns_played = 0
    
    def change_turn(self):
        self.players[0].turn = not self.players[0].turn
        self.players[1].turn = not self.players[1].turn
        
    def quit_game(self, code):
        if (code == self.code and self.num_players > 0):
            self.remove_player()
            return True
        else:
            return False
        
    def drop_token(self, position, addr):
        player = self.players[0]
        if (player.turn == False):
            player = self.players[1]
        if(position > 0 and position <= 7 and player.addr == addr):
            position = position - 1
            row = self.determine_position(position, player.token)
            if (row == -1):
                return False
            self.turns_played += 1
            self.check_winner(player, position, row)
            self.change_turn()
            return True
        return False
    
    def check_winner(self, player, position, row):
        board = self.board
        token = player.token
        horizontal =self.check_horizontal(board, token, row)
        vertical = self.check_vertical(board, token, position)
        diagonal = self.check_diagonal(board, token)
        if (horizontal or vertical or diagonal):
            print (player, "has won!")

    def check_horizontal(self, board, token, row):
        count = 0
        for space in board[row]:
            if (space == token):
                count += 1
            else:
                count == 0
        if (count >= 4):
            return True
        return False
    
    def check_vertical(self, board, token, position):
        count = 0
        for row in board:
            if (row[position] == token):
                count += 1
            else:
                count = 0
        if(count >= 4):
            return True
        return False
    
    def check_diagonal(self, board, token):
        for c in range(len(board[0]) - 3):
            for r in range(len(board) - 3):
                if (board[r][c] == token and \
                    board[r + 1][c + 1] == token and \
                    board[r + 2][c + 2] == token and \
                    board[r + 3][c + 3] == token):
                    return True
        for c in range(len(board[0]) - 3):
            for r in range(3, len(board)):
                if (board[r][c] == token and \
                    board[r - 1][c + 1] == token and \
                    board[r - 2][c + 2] == token and \
                    board[r - 3][c + 3] == token):
                    return True
        return False
    
    def determine_position(self, position, token):
        for row in range(len(self.board) - 1, -1, -1):
            if (self.board[row][position] == " "):
                self.board[row][position] = token
                return row
        return -1

    
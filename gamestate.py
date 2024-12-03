class Player:
    def _init_(self):
        self.token = "O"
        self.addr = None
        self.client = None
        self.turn = False
        self.code = 0
        self.game = None

class Game:
    def __init__(self):
        self.max_players = 2
        self.board_size = 7
        self.players = []
        self.num_spaces = 42
        self.turns_played = 0
        self.board = [[" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "]]
        
    def start_game(self):
        print("Game started!")
        self.board = [[" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " ", " "]]
        player_one = self.players[0]
        player_one.token = "O"
        player_one.turn = True
        player_two = self.players[1]
        player_two.token = "X"
        player_two.turn = False
        self.turns_played = 0
    
    def change_turn(self):
        self.players[0].turn = not self.players[0].turn
        self.players[1].turn = not self.players[1].turn
    
    def add_player(self, addr, client, code):
        player = Player()
        player.addr = addr
        player.client = client
        player.game = self
        player.code = code
        self.players.append(player)
        return player
    
    def remove_player(self, player):
        if (player in self.players):
            print(player)
            self.players.remove(player)

    #This function drops the player's connect 4 token into the board   
    def drop_token(self, position, addr):
        player = self.players[0]
        if (player.turn == False):
            player = self.players[1]
        if(position > 0 and position <= 7 and player.addr == addr):
            position = position - 1
            row = self.determine_position(position, player.token)
            if (row == -1):
                return [False, False]
            self.turns_played += 1
            is_winner = self.check_winner(player, position, row)
            self.change_turn()
            return [True, is_winner]
        return [False, False]
    
    #This function checks after every move if there is a winner, using three helper functions
    def check_winner(self, player, position, row):
        board = self.board
        token = player.token
        horizontal =self.check_horizontal(board, token, row)
        vertical = self.check_vertical(board, token, position)
        diagonal = self.check_diagonal(board, token)
        if (horizontal or vertical or diagonal):
            return True
        return False

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

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
            if (not self.determine_position(position, player.token)):
                return False
            self.turns_played += 1
            self.change_turn()
            return True
        return False
    
    def determine_position(self, position, token):
        for row in range(len(self.board) - 1, -1, -1):
            if (self.board[row][position] == " "):
                self.board[row][position] = token
                return True
        return False

    
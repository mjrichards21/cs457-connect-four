class Game:
    def __init__(self):
        self.num_players = 0
        self.max_players = 2
        self.board_size = 7
        self.player_turn = True
        self.code = 1234

    def get_num_players(self):
        return self.num_players
    
    def add_player(self):
        self.num_players += 1

    def remove_player(self):
        self.num_players -= 1

    def change_turn(self):
        self.player_turn = not self.player_turn

    def join_game(self, code):
        if (code == self.code and self.num_players < self.max_players):
            self.add_player()
            return True
        else:
            return False
        
    def quit_game(self, code):
        if (code == self.code and self.num_players > 0):
            self.remove_player()
            return True
        else:
            return False
        
    def drop_token(self, position):
        if(position > 0 and position <= 7):
            return True
        return False
    
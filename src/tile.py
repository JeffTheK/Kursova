from kivy.uix.button import Button
from kivy.app import App

class Tile(Button):
    def __init__(self, pos, is_bomb, **kwargs):
        super().__init__(**kwargs)
        self._pos = pos
        self.is_bomb = is_bomb
        self.is_flagged = False
        self.is_revealed = False
    
    def flag(self):
        if self.is_revealed:
            return
        board_screen = App.get_running_app().root.get_screen("board")

        if self.is_flagged:
            self.is_flagged = False
            self.remove_widget(self.icon)
            board_screen.score.flagged_tiles -= 1
            if self.is_bomb:
                self.score.correctly_guessed_bombs -= 1
        else:
            self.is_flagged = True
            icon = Image(source="icons/flag.png", size=(self.width / 1.5, self.height / 1.5))
            icon.pos = (self.x + self.width / 2 - icon.width / 2, self.y + self.height / 2 - icon.height / 2)
            self.icon = icon
            self.add_widget(icon)
            board_screen.score.flagged_tiles += 1 # FIXME
            if self.is_bomb:
                board_screen.score.correctly_guessed_bombs += 1 # FIXME
        board_screen.update_bombs_left_label() # FIXME
    
    def reveal(self):
        if self.is_flagged:
            return
        if self.is_bomb:
            self.background_color = (1, 0, 0, 1)
            App.get_running_app().root.get_screen("board").on_game_over()
            self.is_revealed = True
        else:
            self.reveal_non_bomb_tile()
    
    def reveal_non_bomb_tile(self):
        col = self._pos[0]
        row = self._pos[1]
        positions = [
            (col + 1, row),
            (col - 1, row),
            (col, row + 1),
            (col, row - 1),
            (col + 1, row + 1),
            (col - 1, row - 1),
            (col + 1, row - 1),
            (col - 1, row + 1)
        ]

        board_screen = App.get_running_app().root.get_screen("board")

        print(row)
        print(col)
        if self.is_bomb or self.is_revealed:
            return

        self.is_revealed = True
        self.background_color = (0, 0, 0, 0)
        nearby_bombs_count = board_screen.count_nearby_bombs(self._pos)
        if (nearby_bombs_count > 0):
            self.text = str(board_screen.count_nearby_bombs(self._pos))
            self.color = board_screen.nearby_bombs_colors[nearby_bombs_count]
        else:
            for pos_ in positions:
                if board_screen.get_tile_at(pos_) != None:
                    tile = board_screen.get_tile_at(pos_)
                    tile.reveal_non_bomb_tile()
        board_screen.score.cleared_tiles += 1
        board_screen.check_for_win()
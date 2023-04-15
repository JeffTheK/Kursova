from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.config import Config
from kivy.clock import Clock
import random
from tile import Tile
from timer import Timer

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '720')

class MyButton(Button):
    pass

class Difficulty:
    def __init__(self, width, height, bomb_chance) -> None:
        self.width = width
        self.height = height
        self.bomb_chance = bomb_chance

class Score:
    def __init__(self, total_tiles, bombs_count) -> None:
        self.total_tiles = total_tiles
        self.bombs_count = bombs_count
        self.cleared_tiles = 0
        self.correctly_guessed_bombs = 0

class ScoreScreen(Screen):
    score: Score = None

    def on_enter(self):
        self.ids.cleared_tiles_label.text = f"Відкриті комірки: {self.score.cleared_tiles}/{self.score.total_tiles - self.score.bombs_count}"
        self.ids.correctly_guessed_bombs_label.text = f"Правильно позначені бомби: {self.score.correctly_guessed_bombs}/{self.score.bombs_count}"

class BoardScreen(Screen):
    tiles = {}

    nearby_bombs_colors = {
        1: (0, 0, 0, 1),
        2: (0, 0, 1, 1),
        3: (0, 1, 0, 1),
        4: (1, 0, 0, 1),
        5: (0, 0, 0, 1),
        6: (0, 0, 0, 1),
        7: (0, 0, 0, 1),
        8: (0, 0, 0, 1),
    }

    def update_bombs_left_label(self):
        #self.ids.bombs_left_label.text = str(self.score.bombs_count - self.score.flagged_tiles)
        pass

    def restart(self):
        self.setup(self.ids.layout.cols, self.ids.layout.rows, self.bomb_chance)

    def setup(self, difficulty):
        self.setup(difficulty.height, difficulty.width, difficulty.bomb_chance)

    def setup(self, cols, rows, bomb_chance):
        if self.tiles != None:
            for tile in self.tiles.values():
                self.ids.layout.remove_widget(tile)
            self.tiles = {}
        self.ids.layout.cols = cols
        self.ids.layout.rows = rows
        self.ids.timer.start()
        self.bomb_chance = bomb_chance
        bombs_count = 0
        for row in range(rows):
            for col in range(cols):
                is_bomb = random.randrange(0, 100) <= self.bomb_chance
                if is_bomb:
                    bombs_count += 1
                tile = Tile((col, row), is_bomb)
                tile.bind(on_touch_down=lambda _, touch, pos=(col, row): self.on_tile_touch_down(pos, touch))
                #tile.text = str(col) + " " + str(row)
                self.tiles[(col, row)] = (tile)
                self.ids.layout.add_widget(tile)
        self.score = Score(cols * rows, bombs_count)
        self.score.flagged_tiles = 0
        self.update_bombs_left_label()

    def on_tile_touch_down(self, pos, touch):
        tile = self.get_tile_at(pos)
        if not tile.collide_point(*touch.pos):
            return

        if touch.button == "left":
            tile.reveal()
        elif touch.button == "right":
            tile.flag()

    def count_nearby_bombs(self, pos) -> int:
        col = pos[0]
        row = pos[1]
        print("kek" + str(col) + " " + str(row))
        count = 0
        positions = [
            (col + 1, row),
            (col - 1, row),
            (col, row + 1),
            (col, row - 1),
            (col + 1, row + 1),
            (col - 1, row - 1),
            (col + 1, row - 1),
            (col - 1, row + 1)]
        for pos_ in positions:
            print(pos_)
            if self.get_tile_at(pos_) != None and self.get_tile_at(pos_).is_bomb:
                count += 1

        return count
    
    def get_tile_at(self, pos) -> Tile:
        col = pos[0]
        row = pos[1]
        if row > self.ids.layout.rows - 1 or col > self.ids.layout.cols - 1 or row < 0 or col < 0:
            return None
        else:
            return self.tiles[pos]

    def check_for_win(self):
        print(self.score.bombs_count)
        print(self.score.cleared_tiles)
        if (self.score.cleared_tiles + self.score.bombs_count == self.score.total_tiles):
            self.on_win()
            
    def on_win(self):
        App.get_running_app().root.get_screen("score").score = self.score
        App.get_running_app().root.current = "score"

    def on_game_over(self):
        for tile in self.tiles.values():
            if tile.is_bomb:
                icon = Image(source="icons/bomb.png", size=(tile.width / 1.5, tile.height / 1.5))
                icon.pos = (tile.x + tile.width / 2 - icon.width / 2, tile.y + tile.height / 2 - icon.height / 2)
                tile.icon = icon
                tile.add_widget(icon)
        
        def transition_to_stats_screen():
            App.get_running_app().root.current = "score"
        
        App.get_running_app().root.get_screen("score").score = self.score
        Clock.schedule_once(lambda _: transition_to_stats_screen(), 1)

class MainScreen(Screen):
    pass

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MainApp(App):
    pass

MainApp().run()
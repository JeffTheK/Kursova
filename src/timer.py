from kivy.uix.label import Label
from kivy.clock import Clock
import datetime

class Timer(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.datetime.now()
        Clock.schedule_interval(lambda _: self.update(), 1)

    def update(self):
        self.elapsed_time = datetime.datetime.now() - self.start_time
        s = self.elapsed_time.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.text = '{:02}:{:02}'.format(int(minutes), int(seconds))

    def start(self):
        self.start_time = datetime.datetime.now()
        self.text = "00:00"
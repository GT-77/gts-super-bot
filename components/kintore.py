from math import log
from datetime import datetime

dif_scale = 3

bar_hold_dif = 2
v_hold_dif = 1.5
pullup_leniency = 2.5

class DailyChallenge:

    def __init__(self, level):

        self.pushups = int(level)
        self.v_hold = int(v_hold_dif * level)
        self.pullups = int(level / pullup_leniency)
        self.bar_hold = int(self.pullups * bar_hold_dif)



class WorkoutSchedule:

    def __init__(self, deceleration, difficulty, start):

        self.deceleration = deceleration
        self.difficulty = difficulty
        self.start = start

    @classmethod
    def for_gt(cls, deceleration = 10, difficulty = 4, start = datetime(2020, 4, 5)):
        return cls(deceleration, difficulty, start)

    def day(self, d):
        return DailyChallenge(log(d + self.deceleration, self.deceleration) * dif_scale * self.difficulty)
        # https://www.desmos.com/calculator/07jmjwpvrk

    def for_date(self, dt):
        return self.day((dt - self.start).days + 1)

    def for_today(self):
        return self.for_date(datetime.now())

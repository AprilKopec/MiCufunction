from functools import total_ordering
from typing import Union
import re

class Objective:
    def __init__(self, name: str) -> None:
        if re.match(r'^[a-zA-Z0-9_.+-]+$',name) is None:
           raise ValueError(name + " is not a valid objective name")
        self.name = name

# Takes a string which contains either an integer, or an number followed by s or t
# If it's a plain integer or is followed by t, it is interpreted as a number of ticks
# If it's followed by s it is interpreted as a number of seconds
@total_ordering
class Time:
    def __init__(self, time: Union[str, int]) -> None:
        if isinstance(time, str):
            if time[-1] == "s":
                ticks = int(20*float(time[0:-1]))
            elif time[-1] == "t":
                ticks = int(time[0:-1])
            else:
                ticks = int(time)
        else:
            ticks = time
        self.ticks = ticks

    def __add__(self, other):
        return Time(self.ticks + other.ticks)
    def __sub__(self, other):
        return Time(self.ticks - other.ticks)
    def __lt__(self, other):
        return self.ticks < other.ticks
    def __eq__(self, other):
        return self.ticks == other.ticks
    def __str__(self) -> str:
        return str(self.ticks)
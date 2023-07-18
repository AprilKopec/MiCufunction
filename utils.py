from functools import total_ordering
from typing import Union
import re
from math import atan2, degrees, sqrt

class Objective:
    def __init__(self, name: str, criterion = "dummy") -> None:
        if re.match(r'^[a-zA-Z0-9_.+-]+$',name) is None:
           raise ValueError(name + " is not a valid objective name")
        self.name = name
        self.criterion = criterion

    def __str__(self) -> str:
        return self.name

class Score_Holder:
    def __init__(self, name: str) -> None:
        if name[0] == "@":
            raise ValueError("Score holders cannot begin with '@'")
        elif name.isdigit() or (name[0] == "-" and name[1:].isdigit()):
            raise ValueError("Score holder names should not be integers")
        
        self.name = name
    
    def __str__(self) -> str:
        return self.name


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
    def __lt__(self, other) -> bool:
        return self.ticks < other.ticks
    def __eq__(self, other) -> bool:
        return self.ticks == other.ticks
    def __str__(self) -> str:
        return str(self.ticks)

# These should really be methods of Camera_Position but i'm lazy
def parse_coord(r, center):
        r = float(r)
        return r + 0.5 if center else r

# Center if given int, don't if given float
def parse_pos(x, y, z):
    if isinstance(x, str): # slightly hacky
        return (parse_coord(x, "." in x), parse_coord(y, False), parse_coord(z, "." in z))
    else:
        return (float(x), float(y), float(z))

# Probably the simple vector parts here should be replaced with something imported
class Camera_Position:
    def __init__(self, x, y, z, azimuth = 0, altitude = 0):
        self.pos = parse_pos(x, y, z)
        self.angle = (float(azimuth), float(altitude))

    def x(self):
        return self.pos[0]
    
    def y(self):
        return self.pos[1]
    
    def z(self):
        return self.pos[2]
    
    def azimuth(self):
        return self.angle[0]
    
    def altitude(self):
        return self.angle[1]

    def __add__(self, other):
        return Camera_Position(*(self.pos[i] + other.pos[i] for i in range(3)), *(self.angle[i] + other.angle[i] for i in range(2)))
    
    def __sub__(self, other):
        return Camera_Position(*(self.pos[i] - other.pos[i] for i in range(3)), *(self.angle[i] - other.angle[i] for i in range(2)))
    
    def __mul__(self, scalar: float):
        return Camera_Position(*(self.pos[i]*scalar for i in range(3)))
    
    def __truediv__(self, scalar: float):
        return Camera_Position(*(self.pos[i]/scalar for i in range(3)))
    
    def update_pos(self, x, y, z):
        self.pos = parse_pos(x, y, z)

    def update_angle(self, azimuth, altitude):
        self.angle = (float(azimuth), float(altitude))

    # I hate Minecraft's coordinate system
    def facing_to_angle(self, x, y, z):
        target = Camera_Position(x, y, z)
        eyes = self + Camera_Position(0, 1.62, 0)
        direction = target - eyes
        azimuth = atan2(-direction.x(), direction.z())
        altitude = atan2(-direction.y(), sqrt(direction.x()**2 + direction.z()**2))

        azimuth = degrees(azimuth)
        altitude = degrees(altitude)
        return azimuth, altitude

    def face_towards(self, x, y, z):
        self.update_angle(*self.facing_to_angle(x,y,z))

    def slide_per_tick(self, x, y, z, t):
        end = Camera_Position(x, y, z)
        dpos = (end-self)/float(t)
        return dpos.x(), dpos.y(), dpos.z()
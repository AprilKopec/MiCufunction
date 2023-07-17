from utils import Time
from math import atan2, degrees, sqrt

def rest(string, n = 2) -> str:
    return string.split(" ", n)[n]

def block_center(coord):
        assert isinstance(coord,int) or isinstance(coord,float), "Coordinates must be ints or floats"
        return coord + 0.5 if isinstance(coord, int) else coord

def parse_pos(x, y, z):
        return (block_center(x), y, block_center(z))

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
    
    def __div__(self, scalar: float):
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
        self.update_angle(self.facing_to_angle(x,y,z))

    def slide_per_tick(self, x, y, z, t):
        dx = (x-self.x())/t
        dy = (y-self.y())/t
        dz = (z.self.z())/t
        return dx, dy, dz

# Maybe this should be refactored to use a dictionary of subcommands or something
# But recreating a commands system for every complicated command seems slightly silly
# There's probably a good way to do this but I'm too lazy to think of one rn

# If I REALLY HAVE TO I will CONSIDER letting you move the camera to something other than hardcoded coordinates
# But this would necessitate implementing slide through .mcfunction instead of Python
# And that sounds terrible

class Camera:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
        self.parent = stack[-1]
        
        # This is hacky
        self.source = stack[-2] if type(self.parent).__name__ == "Duration" else self.parent

        set_pos = self.source.camera.update_pos
        set_facing = self.source.camera.face_towards
        get_slide_amount = self.source.camera.slide_per_tick

        assert args[1] in ["setup", "summon", "enable", "goto", "slide", "pause", "kill"], "Camera argument not supported"

        if args[1] == "setup":
            self.text = [
                "tp @a[tag=cutsceneCamEnabled] @e[tag=cutsceneCam,limit=1]",
                "execute as @a[tag=cutsceneCamEnabled] at @s rotated as @s run tp @s ^ ^ ^0.1",
                "effect clear @a[tag=!cutsceneCamEnabled,gamemode=adventure] levitation"
            ]
        elif args[1] == "summon":
            assert args[2] == "at", "Syntax is camera summon at X Y Z (facing X Y Z)"
            self.text = [f'kill @e[type=armor_stand,tag=cutsceneCam]']
            # camera summon at X Y Z
            if args[2] == "at":
                self.text += [f'summon armor_stand {args[3]} {args[4]} {args[5]} {{NoGravity:1b,Invulnerable:1b,Invisible:1b,Marker:1b,Tags:["cutsceneCam"]}}']
                set_pos(args[3], args[4], args[5])
                # camera summon at X Y Z facing X Y Z
                if len(args) > 6:
                    assert args[6] == "facing", "Only supported syntax is 'facing'"
                    assert len(args) == 10, "'facing' takes XYZ coordinates of a block the camera is facing towards"
                    self.text += [f"execute as @e[tag=cutsceneCam] at @s facing {args[7]} {args[8]} {args[9]} run tp @s ~ ~ ~ ~ ~"]
                    set_facing(args[7], args[8], args[9])
        # camera enable {target selector}
        elif args[1] == "enable":
            if len(args = 2):
                target = "@a[gamemode=adventure]"
            else:
                target = rest(line, 2)
            self.text = [
                f"tag {target} add cutsceneCamEnabled",
                f"effect give {target} levitation infinite 255 true",
                f"gamemode spectator {target}"
                ]
        # camera goto
        elif args[1] == "goto":
            # camera goto X Y Z
            if len(args) == 5:
                    self.text = [f'execute positioned {args[2]} {args[3]} args{[4]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~']
                    set_pos(args[2], args[3], args[4])
            # camera goto X Y Z facing X Y Z
            else:
                assert args[5] == "facing", "Only supported syntax is 'camera goto X Y Z (facing X Y Z)'"
                assert len(args) == 9, "'facing' takes XYZ coordinates of a block the camera is facing towards"
                self.text = [f'execute positioned {args[2]} {args[3]} {args[4]} facing {args[6]} args{[7]} args{[8]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~']
                set_facing(args[6], args[7], args[8])
        # slide is currently implemented in Python
        # It will be much more versatile if implemented in .mcfunction but I don't wanna
        # I will consider implementing that once I can compile a .micufunction to do the scoreboard awful for me
        # Consequently slide will break if it follows an if block without a goto inbetween
        elif args[1] == "slide":
            assert args[2] in ["to", "by"], "Syntax is 'camera slide to' or 'camera slide by'"
            if args[2] == "to":
                assert type(self.parent).__name__ == "Duration", "camera slide to must be inside duration block"
                assert len(args) == 6, "Automatic angle calculation not supported until .micufunction can do scoreboard math well"
                dx, dy, dz = get_slide_amount(args[3], args[4], args[5], self.parent.duration.ticks)
                self.text = [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{dx} ~{dy} ~{dz} ~ ~']
                set_pos(args[3], args[4], args[5])
            elif args[2] == "by":
                assert len(args) in [6, 8], "Syntax is 'camera slide by DX DY DZ (DANGLEX DANGLEY)"
                t = self.parent.duration.ticks if type(self.parent).__name__ == "Duration" else 1
                if len(args) == 6:
                    self.text = [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{args[3]} ~{args[4]} ~{args[5]} ~ ~']
                    self.source.camera += Camera_Position(args[3], args[4], args[5])*t
                elif len(args) == 8:
                    self.text = [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{args[3]} ~{args[4]} ~{args[5]} ~{args[6]} ~{args[7]}']
                    self.source.camera += Camera_Position(args[3], args[4], args[5], args[6], args[7])*t
        elif args[1] == "pause":
            assert len(args) == 2, "camera pause doesn't take any further arguments"
            target = "@a[tag=cutsceneCamEnabled]"
            self.text = [
                f"effect clear {target} levitation",
                f"gamemode adventure {target}",
                f"tag {target} remove cutsceneCamEnabled"
                ]
        elif args[1] == "kill":
            assert len(args) == 2, "camera kill doesn't take any further arguments"
            target = "@a[tag=cutsceneCamEnabled]"
            self.text = [
                f"effect clear {target} levitation",
                f"gamemode adventure {target}",
                f"tag {target} remove cutsceneCamEnabled",
                " ".join(self.parent.prefix), f"kill @e[type=armor_stand,tag=cutsceneCam]"
            ]

        if args[1] != "setup":
            self.text = [" ".join[self.parent.prefix(), line] for line in self.text]

from utils import Time
from math import atan2, degrees, sqrt

def rest(string, n = 2) -> str:
    return string.split(" ", n)[n]

# Probably the simple vector parts here should be replaced with something imported
class Camera_Position:
    def __init__(self, x, y, z, azimuth = 0, altitude = 0):
        self.pos = (float(x), float(y), float(z))
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
        return Camera_Position(*(self.pos[i] + other.pos[i] for i in range(3)))
    
    def __sub__(self, other):
        return Camera_Position(*(self.pos[i] - other.pos[i] for i in range(3)))
    
    def __mul__(self, scalar: float):
        return Camera_Position(*(self.pos[i]*scalar for i in range(3)))
    
    def __div__(self, scalar: float):
        return Camera_Position(*(self.pos[i]/scalar for i in range(3)))
    
    def update_pos(self, x, y, z):
        self.pos = (float(x), float(y), float(z))

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

    def slide_to_pos(self, x, y, z, t):
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

        if args[1] == "setup":
            # The lack of prefix here is intentional; this should run the entire duration of the function
            self.text = [
                "tp @a[tag=cutsceneCamEnabled] @e[tag=cutsceneCam,limit=1]",
                "execute as @a[tag=cutsceneCamEnabled] at @s rotated as @s run tp @s ^ ^ ^0.1",
                "effect clear @a[tag=!cutsceneCamEnabled,gamemode=adventure] levitation"
            ]
        elif args[1] == "summon":
            assert len(args) > 2, "You must specify a camera position"
            assert args[2] == "at", "Supported camera summon arguments are 'at' and 'execute'"
            self.text = [" ".join(self.parent.prefix(), f'kill @e[type=armor_stand,tag=cutsceneCam]')]
            # camera summon at X Y Z
            if args[2] == "at":
                self.text += [" ".join(self.parent.prefix(), f'summon armor_stand {args[3]} {args[4]} {args[5]} {{NoGravity:1b,Invulnerable:1b,Invisible:1b,Marker:1b,Tags:["cutsceneCam"]}}')]
                set_pos(args[3], args[4], args[5])
                # camera summon at X Y Z facing X Y Z
                if len(args) > 6:
                    assert args[6] == "facing", "Only supported syntax is 'facing'"
                    assert len(args) == 10, "'facing' takes XYZ coordinates of a block the camera is facing towards"
                    self.text += [" ".join(self.parent.prefix(), f"execute as @e[tag=cutsceneCam] at @s facing {args[7]} {args[8]} {args[9]} run tp @s ~ ~ ~ ~ ~")]
                    set_facing(args[7], args[8], args[9])
        # camera enable {target selector}
        elif args[1] == "enable":
            if len(args = 2):
                target = "@a[gamemode=adventure]"
            else:
                target = rest(line, 2)
            self.text = [
                " ".join(self.parent.prefix(), f"tag {target} add cutsceneCamEnabled"),
                " ".join(self.parent.prefix(), f"effect give {target} levitation infinite 255 true")
                ]
        # camera goto
        elif args[1] == "goto":
            # camera goto X Y Z
            if len(args) == 5:
                    self.text = [" ".join(self.parent.prefix(), f'execute positioned {args[2]} {args[3]} args{[4]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~')]
                    set_pos(args[2], args[3], args[4])
            # camera goto X Y Z facing X Y Z
            else:
                assert args[5] == "facing", "Only supported syntax is 'facing'"
                assert len(args) == 9, "'facing' takes XYZ coordinates of a block the camera is facing towards"
                self.text = [" ".join(self.parent.prefix(), f'execute positioned {args[2]} {args[3]} {args[4]} facing {args[6]} args{[7]} args{[8]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~')]
                set_facing(args[6], args[7], args[8])
        elif args[1] == "slide":
            assert args[2] == "to", "Syntax is 'camera slide to'"
            assert type(self.parent).__name__ == "Duration", "camera slide must be inside duration block"




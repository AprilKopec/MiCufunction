from utils import Camera_Position
from command_baseclass import MiCufunction_Command

def rest(string, n = 2) -> str:
    return string.split(" ", n)[n]

# If I REALLY HAVE TO I will CONSIDER letting you move the camera to something other than hardcoded coordinates
# But this would necessitate implementing slide through .mcfunction instead of Python
# And that sounds terrible

class Camera(MiCufunction_Command):
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
        super().__init__(stack, line, args)
        self.parent = stack[-1]
        
        # This is hacky
        self.source = stack[-2] if type(self.parent).__name__ == "Duration" else self.parent

        # Some of this should maybe not be directly in __init__
        self.set_pos = self.source.camera.update_pos
        self.set_facing = self.source.camera.face_towards
        self.get_slide_amount = self.source.camera.slide_per_tick

        subcommand_dict = {
            "setup": self.setup,
            "summon": self.summon,
            "enable": self.enable,
            "goto": self.goto,
            "slide": self.slide,
            "pause": self.pause,
            "kill": self.kill
        }

        assert args[1] in subcommand_dict, "Camera argument not supported"
        self.text = subcommand_dict[args[1]](args[2:])

        if args[1] != "setup":
            self.text = [self.add_prefix(line) for line in self.text]

    def setup(self, args):
        return [
                "tp @a[tag=cutsceneCamEnabled] @e[tag=cutsceneCam,limit=1]",
                "execute as @a[tag=cutsceneCamEnabled] at @s rotated as @s run tp @s ^ ^ ^0.1"
            ]
            
    def summon(self, args):
        assert args[0] == "at", "Syntax is camera summon at X Y Z (facing X Y Z)"
        text = [f'kill @e[type=armor_stand,tag=cutsceneCam]']
        # camera summon at X Y Z
        if args[0] == "at":
            text += [f'summon armor_stand {args[1]} {args[2]} {args[3]} {{NoGravity:1b,Invulnerable:1b,Invisible:1b,Marker:1b,Tags:["cutsceneCam"]}}']
            self.set_pos(args[1], args[2], args[3])
            # camera summon at X Y Z facing X Y Z
            if len(args) > 4:
                assert args[4] == "facing", "Only supported syntax is 'facing'"
                assert len(args) == 8, "'facing' takes XYZ coordinates of a block the camera is facing towards"
                text += [f"execute as @e[tag=cutsceneCam] at @s facing {args[5]} {args[6]} {args[7]} run tp @s ~ ~ ~ ~ ~"]
                self.set_facing(args[5], args[6], args[7])
        return text

    # camera enable {target selector}
    def enable(self, args):
        if len(args) == 0:
            target = "@a[gamemode=adventure]"
        else:
            target = rest(self.line, 2)
        return [
            f"tag {target} add cutsceneCamEnabled",
            f"effect give {target} levitation infinite 255 true",
            f"gamemode spectator {target}"
            ]
    
    def goto(self, args):
        # camera goto X Y Z
        assert len(args) > 2, "camera goto takes X Y Z coordinates as arguments"
        self.set_pos(args[0], args[1], args[2])
        if len(args) == 3:
                return [f'execute positioned {args[0]} {args[1]} args{[2]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~']     
        # camera goto X Y Z facing X Y Z
        else:
            assert args[3] == "facing", "Only supported syntax is 'camera goto X Y Z (facing X Y Z)'"
            assert len(args) == 7, "'facing' takes XYZ coordinates of a block the camera is facing towards"
            self.set_facing(args[4], args[5], args[6])
            return [f'execute positioned {args[0]} {args[1]} {args[2]} facing {args[4]} args{[5]} args{[6]} run tp @e[tag=cutsceneCam] ~ ~ ~ ~ ~']

    # slide is currently implemented in Python
    # It will be much more versatile if implemented in .mcfunction but I don't wanna
    # I will consider implementing that once I can compile a .micufunction to do the scoreboard awful for me
    # Consequently slide will break if it follows an if block without a goto inbetween
    def slide(self, args):
        assert args[0] in ["to", "by"], "Syntax is 'camera slide to' or 'camera slide by'"
        if args[0] == "to":
            assert type(self.parent).__name__ == "Duration", "camera slide to must be inside duration block"
            assert len(args) == 4, "Automatic angle calculation not supported until .micufunction can do scoreboard math well"
            dx, dy, dz = self.get_slide_amount(args[1], args[2], args[3], self.parent.duration.ticks)
            self.set_pos(args[1], args[2], args[3])
            return [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{dx} ~{dy} ~{dz} ~ ~'] 
        elif args[0] == "by":
            assert len(args) in [4, 6], "Syntax is 'camera slide by DX DY DZ (DANGLEX DANGLEY)"
            t = self.parent.duration.ticks if type(self.parent).__name__ == "Duration" else 1
            if len(args) == 4:
                self.source.camera += Camera_Position(args[1], args[2], args[3])*t
                return [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{args[1]} ~{args[2]} ~{args[3]} ~ ~']
            elif len(args) == 6:
                self.source.camera += Camera_Position(args[1], args[2], args[3], args[4], args[5])*t
                return [f'execute as @e[tag=cutsceneCam] at @s rotated as @s run tp @s ~{args[1]} ~{args[2]} ~{args[3]} ~{args[4]} ~{args[5]}']
    
    def pause(self, args):
        assert len(args) == 0, "camera pause doesn't take any further arguments"
        target = "@a[tag=cutsceneCamEnabled]"
        return [
            f"effect clear {target} levitation",
            f"gamemode adventure {target}",
            f"tag {target} remove cutsceneCamEnabled"
            ]
        
    def kill(self, args):
        assert len(args) == 0, "camera kill doesn't take any further arguments"
        return self.pause(args) + [f"kill @e[type=armor_stand,tag=cutsceneCam]"]

        

# MiCufunction
MiCufunction is a .mcfunction scripting language compiled using Python3. It mainly makes creating timed sequences of events much easier; it tracks a timer for you, rather than you having to make a timer yourself and manually sum up delays and so on. It also has a camera system, if you want to slide the player's perspective over a region or something, and various other convenience features.

To compile, run `MiCufunction.py [file path to .micufunction file] [root data pack folder]` on a command line. Xero has some scripts for automatically pulling a data pack from GitHub and compiling all of the .micufunction files in it which you can probably ask him for if you want. 

Here is an example .micufunction:
```
function test:test1 {
    say <Character A> Hello!
    # This is a comment
    wait 10
    duration 30t {
        command execute as @a at @s run tp @s ~ ~1 ~
    }
    if score Money Stats matches 20.. {
        say You upgraded your item!
    } else {
        say You cannot afford to upgrade your item.
    }
}
```

This code compiles to a .mcfunction which, when ran, will output "<Character A> hi" to chat on the first tick, teleport everyone up by one block each tick for thirty ticks beginning on the eleventh tick, and then on the 41st tick will output text to chat depending on whether you have 20 Money or not. 

Currently supported commands:
- `function`
- `wait`
- `command`
- `say`
- `duration`
- `if` / `else`
- `camera`

## function
`function` takes a namespaced function title as an argument—it should be the same as the argument that /function will take in Minecraft. It starts with a namespace `[namespace]:` and then the file location relative to the `data/[namespace]/functions` folder. (Don't add .mcfunction at the end of the argument).

`function` opens a code block and will produce a `.mcfunction` file that implements the contents of the code block.

## wait
`wait` takes a duration, which can be written in either ticks or seconds. If using ticks you can either just write an integer or write an integer with t appended. If using seconds you append s to the integer. So `20`, `20t`, and `1s` all do the same thing. You can also do `1.5s`, which gets casted to an integer number of ticks. (It might be best use ticks rather than fractional seconds if rounding might cause issues.)

`wait` is supported inside functions, `if` blocks, and `else` blocks. Do not put `wait` inside a `duration` block.

## command
`command` takes a minecraft command as an argument and runs the command.

## say
`say` takes text as an argument and outputs the text to chat.

## duration
`duration` takes a duration the same way wait does, and runs the commands inside a code block on each tick for that amount of time. `duration` code blocks should only contain `say` and `command`; if you want to run something conditionally in a `duration` you should do `command execute if ...`. 

`duration` does not update the cutscene timer; the contents of a `duration` block will run in parallel with any code following the `duration` block. Consequently, it is not (currently) supported to have an `if` block overlapping a `duration` block; make sure any `duration`s have concluded before you open an `if`.

## if / else
`if` runs a subcutscene based on an `execute condition``. An execute condition `execute if` subcommand. The above example uses `score Lemmata Stats matches 20..`, which is a condition that might appear in a command like `execute if score Lemmata Stats matches 20.. run ...`.

`else` works the same as `if`, but it evaluates the condition as its opposite

## camera
The camera command is an interface for moving around the player as a camera in spectator mode. I (April) didn't focus too hard on making this *incredibly* easy to use for people other than me, but I don't think it's too too complicated.
Optional subcommands are in parentheses.

### camera setup
Put this at the top of any micufunction where you intend to use the camera system. It adds the commands that teleport the player to the camera every tick (when the camera is enabled).

### camera summon at [X] [Y] [Z] (facing [X2] [Y2] [Z2])
Places the camera at the block [X] [Y] [Z] as if the player ran a /tp command there.
Faces the camera towards the center of the block X2 Y2 Z2.

### camera enable (target)
Turn the camera on (put the player in spectator mode, enable tping to the camera every tick).
Specifically it turns the camera on for `target`, which defaults to `@a[gamemode=adventure]`.

### camera goto [X] [Y] [Z] (facing [X2] [Y2] [Z2])
This works like `summon`, except when you already have a camera around.

### camera slide
This command is used to slide the camera. It has two versions.

#### camera slide to [X] [Y] [Z]
This command relies on being inside a `duration` block. It automatically calculates and applies the offset required to move the camera from the position it was in before the `duration` block to [X] [Y] [Z] over the course of the `duration` block.

`camera slide to`'s implementation currently relies on state stored in the Python execution of the program. This means it doesn't play particularly well with `if` blocks. If you move the camera during an `if` block, and then try to `slide` afterwards, the offset calculation won't use the updated position, because the Python program could not tell which branch of the condition would be ran.

tl;dr if you want to use `camera slide to` then you should make sure you have done a `goto` since any `if` blocks which move the camera.

#### camera slide by [dx] [dy] [dz] ([danglex] [dangley])
This slides by a specified offset each tick of a `duration` block. I think technically you could also use it outside of a duration block if you wanted to just move the camera by a certain relative amount.

### camera pause
This leaves the camera entity around, but detaches the player from the camera and puts them back in adventure mode. You can unpause it with `enable` if you want.

### camera kill
This detaches the player from the camera and then kills the camera entity.
You should run this at the end of any cutscene that uses the camera.

# Planned features
Some of these are partially implemented
- Variables
- `execute condition` data type
- `elif`
- `wait until/while [execute condition]`
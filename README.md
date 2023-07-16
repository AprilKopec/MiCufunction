# MiCufunction
MiCufunction is a .mcfunction scripting language using Python3.

How to compile:
TODO: implement compilation

Here is an example .micufunction:
```
function tt2:misc/example_micufunction {
    say <Miku> hi
    # This is a comment
    wait 10
    duration 30t {
        command gamemode creative @a
        say <Miku> hello!
    }
    if score Lemmata Stats matches 20.. {
        say Your mathematical intuition says you have at least 20 lemmata.
    } else {
        say Your mathematical intuition says you do not have 20 lemmata.
        wait 4s
        say Your mathematical intuition calls you a fool.
    }
}
```

This code compiles to a .mcfunction which, when ran, will output "<Miku> hi" to chat on the first tick, set everyone to creative and spam chat with "<Miku> hello!" for thirty ticks beginning on the eleventh tick, and then on the 41st tick will output text to chat depending on whether you have 20 lemmata or not. 

Currently supported commands:
- `function`
- `wait`
- `command`
- `say`
- `duration`
- `if` / `else`

## function
`function` takes a namespaced function title as an argument—it should be the same as the argument that /function will take in Minecraft. It starts with `tt2:` (or another datapack namespace) and then the file location relative to the tt2/functions folder. (Don't add .mcfunction at the end of the argument).

`function` opens a code block and will produce a `.mcfunction` file that implements the contents of the code block.

## wait
`wait` takes a duration, which can be written in either ticks or seconds. If using ticks you can either just write an integer or write an integer with t appended. If using seconds you append s to the integer. So `20`, `20t`, and `1s` all do the same thing. You can also do `1.5s`, which gets casted to an integer number of ticks. (Probably just don't do this for now until I verify how rounding works.)

`wait` is supported inside functions, `if` blocks, and `else` blocks. Do not put `wait` inside a `duration` block.

## command
`command` takes a minecraft command as an argument and runs the command.

## say
`say` takes text as an argument and outputs the text to chat.

## duration
`duration` takes a duration the same way wait does, and runs the commands inside a code block on each tick for that amount of time. `duration` code blocks should only contain `say` and `command`; if you want to run something conditionally in a `duration` you should do `command execute if ...`. 

`duration` does not update the cutscene timer; the contents of a `duration` block will run in parallel with any code following the `duration` block. Consequently, it is not (currently) supported to have an `if` block overlapping a `duration` block; make sure any `duration`s have concluded before you open an `if`.

## if / else
`if` runs code based on a certain condition. The argument `if` takes is a condition which can be evaluated by the `execute if` subcommand. The above example uses `score Lemmata Stats matches 20..`, which is a condition that might appear in a command like `execute if score Lemmata Stats matches 20.. run ...`.

`else` works the same as `if`, but it evaluates the condition as `execute unless` instead.

if probably needs some work.
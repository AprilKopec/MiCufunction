# MiCufunction
 MiCufunction -> mcfunction compiler

```
cutscene {
    say <Miku> hi
    # This is a comment
    wait 10
    command gamemode creative @a
}
```

should compile to
```
### Cutscene setup ###
scoreboard objectives add <ObjectiveName> dummy
scoreboard players add t <ObjectiveName> 1
scoreboard players set endCutscene <ObjectiveName> 0

### Cutscene ###
execute if score t <ObjectiveName> matches 1 run tellraw @a "<Miku> hi"
# This is a comment
execute if score t <ObjectiveName> matches 11 run gamemode creative @a

### Cutscene cleanup ###
execute if score t <ObjectiveName> matches 11 run scoreboard players set endCutscene <ObjectiveName> 1
execute if score endCutscene <ObjectiveName> matches 1 run scoreboard players set t <ObjectiveName> 0

### Run cutscene every tick ###
execute unless score endCutscene <ObjectiveName> matches 1 run schedule function <this function> 1t append
```
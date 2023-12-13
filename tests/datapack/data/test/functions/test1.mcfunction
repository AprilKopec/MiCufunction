### Cutscene setup ###
scoreboard objectives add test.test1 dummy
execute unless score pause test.test1 matches 1 run scoreboard players add t test.test1 1
scoreboard players set end test.test1 0

### Cutscene ###
execute if score t test.test1 matches 1 run tellraw @a "<Character A> Hello!"
# This is a comment
execute if score t test.test1 matches 11..40 run execute as @a at @s run tp @s ~ ~1 ~
    execute if score t test.test1 matches 11 run execute if score Money Stats matches 20.. run scoreboard players set condition1 test.test1 1
    execute if score t test.test1 matches 11 run execute unless score condition1 test.test1 matches 1 run scoreboard players set condition1 test.test1 0
    execute if score t test.test1 matches 11 run scoreboard players set end1 test.test1 0
    execute if score t test.test1 matches 11 run scoreboard players add t test.test1 1
    execute if score t test.test1 matches 12 run scoreboard players set pause test.test1 1
    execute if score t test.test1 matches 12 run execute unless score pause1 test.test1 matches 1 run scoreboard players add t1 test.test1 1

    execute if score t test.test1 matches 12 run execute if score condition1 test.test1 matches 1 if score t1 test.test1 matches 1 run tellraw @a "You upgraded your item!"

    execute if score t test.test1 matches 12 run execute if score condition1 test.test1 matches 1 if score t1 test.test1 matches 1 run scoreboard players set end1 test.test1 1

    execute if score t test.test1 matches 12 run execute if score condition1 test.test1 matches 0 if score t1 test.test1 matches 1 run tellraw @a "You cannot afford to upgrade your item."

    execute if score t test.test1 matches 12 run execute if score condition1 test.test1 matches 0 if score t1 test.test1 matches 1 run scoreboard players set end1 test.test1 1
execute if score t test.test1 matches 12 run execute if score end1 test.test1 matches 1 run scoreboard players set t1 test.test1 0
execute if score t test.test1 matches 12 run execute if score end1 test.test1 matches 1 run scoreboard players set condition1 test.test1 -1
execute if score t test.test1 matches 12 run execute if score end1 test.test1 matches 1 run scoreboard players set pause test.test1 0
execute if score t test.test1 matches 12 run execute if score end1 test.test1 matches 1 run scoreboard players add t test.test1 1

### Cutscene Cleanup ###
execute if score t test.test1 matches 31 run scoreboard players set end test.test1 1
execute if score end test.test1 matches 1 run scoreboard players set t test.test1 0

### Run cutscene every tick ###
scoreboard players operation global_timer test.test1 -= t Tt2GlobalTimer
execute if score global_timer test.test1 matches 0 run scoreboard players set force_quit test.test1 1
scoreboard players operation global_timer test.test1 = t Tt2GlobalTimer
execute unless score end test.test1 matches 1 unless score force_quit test.test1 matches 1 run schedule function test:test1 1t replace

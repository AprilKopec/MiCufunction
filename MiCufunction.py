import sys
import re

filename = sys.argv[1]
outname = sys.argv[2]

# Checks if a string is a valid scoreboard objective name
def validate_objective_name(str):
    return re.match(r'^[a-zA-Z0-9_.+-]+$',str) is not None

# Takes a string which contains either an integer, or an number followed by s or t
# If it's a plain integer or is followed by t, it is interpreted as a number of ticks
# If it's followed by s it is interpreted as a number of seconds
def get_time(str):
    if str[-1] == "s":
        return int(20*float(str[0:-1]))
    elif str[-1] == "t":
        return int(str[0:-1])
    try:
        return int(str)
    except ValueError as e:
        raise e(f"{str} is not in an accepted time format")

if(filename.split('.')[-1].lower() != "micufunction"):
    raise Exception(".micufunction file not provided")

outlines = []
stack = []

with open(filename, 'r') as infile:
    lines = infile.readlines
    for line in lines:
        line = line.strip()
        split = line.split(' ')

        if split[0] == "cutscene":
            stack.append("cutscene")

            ObjectiveName = split[1]
            if not validate_objective_name(ObjectiveName):
                raise Exception("Invalid scoreboard objective name")
            
            time = 1

            finish_time = 1
            
            outlines.append("### Cutscene setup ###")
            outlines.append(f"scoreboard objectives add {ObjectiveName} dummy")
            outlines.append(f"scoreboard players add t {ObjectiveName} 1")
            outlines.append(f"scoreboard players set endCutscene {ObjectiveName} 0")
            outlines.append("")
            outlines.append("### Cutscene ###")

        if split[0] == "duration":
            if stack[-1] == "cutscene":
                stack.append("duration")
                duration = get_time(split[1])
                finish_time = time+duration

        if split[0] == "say":
            if stack[-1] == "cutscene":
                outlines.append(f'execute if score t {ObjectiveName} matches {time} run tellraw @a "{line[4:]}"')
            elif stack[-1] == "duration":
                outlines.append(f'execute if score t {ObjectiveName} matches {time}..{time+duration} run tellraw @a "{line[4:]}"')

        if split[0] == "command":
            if stack[-1] == "cutscene":
                outlines.append(f"execute if score t {ObjectiveName} matches {time} run {line[8:]}")
            elif stack[-1] == "duration":
                outlines.append(f'execute if score t {ObjectiveName} matches {time}..{time+duration}')

        if split[0] == "wait":
            if stack[-1] == "cutscene":
                time += get_time(split[1])
            elif stack[-1] == "duration":
                raise Exception("Putting wait inside duration is not a feature")
            
        if split[0] == "}":
            block = stack.pop()
            if block == "cutscene":
                finish_time = max(finish_time, time)

                outlines.append("")
                outlines.append("### Cutscene Cleanup ###")
                outlines.append(f'execute if score t {ObjectiveName} matches {finish_time} run scoreboard players set endCutscene {ObjectiveName} 1')
                outlines.append(f'execute if score endCutscene {ObjectiveName} matches 1 run scoreboard players set t {ObjectiveName} 0')
                outlines.append("")
                outlines.append("### Run cutscene every tick ###")
                outlines.append(f"execute unless score endCutscene {ObjectiveName} matches 1 run schedule function {outname} 1t append")

            elif block == "duration":
                pass

            else:
                raise Exception("You tried to use an invalid block type or something")

for line in outlines:
    print(line)
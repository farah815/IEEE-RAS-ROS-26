def move_player(position, direction):
    x, y = position

    if direction == "up":
        y += 1
    elif direction == "down":
        y -= 1
    elif direction == "right":
        x += 1
    elif direction == "left":
        x -= 1
    else:
        return "Invalid direction!"

    return (x, y)

start = (0, 0)

print(move_player(start, "up"))
print(move_player(start, "down"))
print(move_player(start, "right"))
print(move_player(start, "left"))
print(move_player(start, "jump"))
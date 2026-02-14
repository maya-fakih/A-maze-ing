width = 20

height = 20

num = 20

for i in range(width):
    forward = True
    path = []
    if forward:
        j1 = width // 2 - i
        j2 = width // 2 + 1 + i
    else:
        j1 = width // 2 + j
        j2 = width // 2 - j
        j += 1
    if j1 < 0:
        forward = False
        j = 0

    path.extend([(i, j1), (i, j2)])

for i in range(width):
    for j in range(height):
        if (i, j) in path:
            print("*", end="")
        else:
            print("", end="")
    print()

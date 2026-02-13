width = 20

height = 20

for row in range(width):
    for col in range(height):
        if (row - col) == (width // 2) or (row + col) == (width // 2) or (row + col) == (width // 2)**2:
            print("*", end = "")
        else:
            print("", end = "")
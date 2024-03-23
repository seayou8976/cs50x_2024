import cs50

while True:
    height = cs50.get_int("Height: ")
    if height in range(1, 9):
        break

for i in range(height):
    num_space = height - (i + 1)
    num_hash = i + 1
    print(f"{' ' * num_space}{'#' * num_hash}  {'#' * num_hash}")

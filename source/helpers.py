def get_dimension():
    while True:
        dimension = input("Enter a maze dimension: ")
        if dimension == "":
            return 40
        else:
            try:
                int(dimension)
            except ValueError:
                print("ERROR: Invalid Dimension")

            return int(dimension)


def init_dimension() -> int:
    print('-----------------------Maze Generator & Solver-----------------------')
    dimension = get_dimension()
    print('The goal is to get from the green square in the top left')
    print('to the green square in the bottom right!')
    print('Controls:')
    print("Generate maze ---------------------------------------------> hit 'Space'")
    print("Generate solution using a depth-first recursive algorithm -----> hit '1'")
    print("Generate solution using a breadth-first brute force algorithm -> hit '2'")

    return dimension

def get_rerun():
    temp = input("Would you like to re run the program? (y/n): ")
    return temp.lower() == 'y'
import random
import queue


def printPuzzle(puzzle):
    """
    Print the current representation of the puzzle
    """
    for row in range(len(puzzle)):
        rowLine = ""
        for col in puzzle[row]:
            rowLine += str(col) + " "
        print(rowLine)


def maze_representation(n=20): #optional parameter
    """
    Generate the n x n puzzle with only allowable numbers
    """
    ##validate user input is between 5-10
    if n == 20:
        while n < 5 or n > 10:
            if n == 0:
                n = int(input("Rook Jumping Maze Size (5-10): "))
            else:
                n = int(input("Please only choose numbers 5-10: "))
    ##initialize the puzzle as all 0's
    puzzle = [[0 for element in range(n)] for element in range(n)]
    ##populate the puzzle board
    for i in range(n):
        for j in range(n):
            choices = []
            # if its the goal cell
            if i == n-1 and j == n-1:
                puzzle[i][j] = 0
            else:
                rmax = n - 1
                rmin = 0
                cmax = n - 1
                cmin = 0
                r = i
                c = j
                #max legal number function provided
                max_ = max(rmax - r, max(r - rmin, max(cmax - c, c-cmin)))
                #randomly choose from list of legal numbers
                choices = list(range(1,max_ + 1))
                puzzle[i][j] = random.choice(choices)
    return puzzle


def maze_evaluation(puzzle):
    """
    Find a solution to the maze if there is one, and return the solution depth if it exists
    The lower the return value number, the harder the maze
    """
    n = len(puzzle)
    max_index = n - 1
    actions = ["L","R","U","D"] #left/right/up/down
    visited = []
    solution = [] #path to goal from start
    #### (r, c, direction, parent node)
    root = (0,0,"Root",None)
    q = queue.Queue()
    q.put(root)
    sol = False
    while(not q.empty() and not sol):
        curr = q.get()
        i, j, direction, parent = curr
        if (i,j, direction) not in visited:
            value = puzzle[i][j]
            if value == 0:
                sol = True
                depth = 0
                last = visited[len(visited)-1]
                while last != root:
                    r, c, move, last = last
                    solution.append(move)
                    depth = depth - 1
                solution = list(reversed(solution))
                print("Solution:", solution)
            else:
                for action in actions:  #translate actions to index moves
                    if action == "U":
                        if i-value >= 0 and i-value <= max_index:
                            if (i-value,j, action, curr) not in visited:
                                q.put((i-value,j, action, curr))
                    elif action == "D":
                        if i+value >= 0 and i+value <= max_index:
                            if (i+value,j, action, curr) not in visited:
                                q.put((i+value,j,action, curr))
                    elif action == "L":
                        if j-value >= 0 and j-value <= max_index:
                            if (i,j-value, action, curr) not in visited:
                                q.put((i,j-value, action, curr))
                    else: #"R"
                        if j+value >= 0 and j+value <= max_index:
                            if (i,j+value, action, curr) not in visited:
                                q.put((i,j+value,action, curr))
            visited.append((curr))
        if q.qsize() > 1000 or len(visited) > 300:
            return 1000000
    return depth

def maze_generation(n, x, eval=False):
    """
    Generates a maze and changes indexes in it, to see if it makes the maze harder
    """
    puzzle = maze_representation(n)
    currEval = maze_evaluation(puzzle)
    originalEval = currEval
    i = random.randrange(0, n)
    j = random.randrange(0, n)
    while i == n-1 and j == n-1: #prevent it from selecting goal state
        i = random.randrange(0, n)
        j = random.randrange(0, n)
    for times in range(x):      #iterations on jump value change
        tempPuzzle = puzzle
        bound = max((n-1) - i, max(j - 0, max((n-1) - j, j-0)))
        currValue = tempPuzzle[i][j]
        newValue = random.randrange(1, bound+1)
        while newValue == currValue:
            newValue = random.randrange(1, bound+1)
        tempPuzzle[i][j] = newValue
        tempEval = maze_evaluation(tempPuzzle)
        if tempEval <= currEval:
            puzzle = tempPuzzle
            currEval = tempEval
    if eval:
        print(currEval - originalEval, "better for: ", x, " iterations.")
    return puzzle


def random_restarts(n, restarts, x, eval=False):
    """
    Performs First Choice Descent iteratively with random restarts
    """
    puzzle = maze_representation(n)
    currEval = maze_evaluation(puzzle)
    originalEval = currEval
    for x in range(restarts):
        i = random.randrange(0, n)
        j = random.randrange(0, n)
        while i == n-1 and j == n-1:
            i = random.randrange(0, n)
            j = random.randrange(0, n)
        for times in range(x):
            tempPuzzle = puzzle
            bound = max((n-1) - i, max(j - 0, max((n-1) - j, j-0)))
            currValue = tempPuzzle[i][j]
            newValue = random.randrange(1, bound+1)
            while newValue == currValue:
                newValue = random.randrange(1, bound+1)
            tempPuzzle[i][j] = newValue
            tempEval = maze_evaluation(tempPuzzle)
            if tempEval <= currEval:
                puzzle = tempPuzzle
                currEval = tempEval
    if eval:
        print(currEval - originalEval, "better for: ", restarts, " restarts.")
    return puzzle

def uphill(n, x, prob, eval=False):
    puzzle = maze_representation(n)
    currEval = maze_evaluation(puzzle)
    originalEval = currEval
    i = random.randrange(0, n)
    j = random.randrange(0, n)
    while i == n-1 and j == n-1: #prevent it from selecting goal state
        i = random.randrange(0, n)
        j = random.randrange(0, n)
    for times in range(x):      #iterations on jump value change
        tempPuzzle = puzzle
        bound = max((n-1) - i, max(j - 0, max((n-1) - j, j-0)))
        currValue = tempPuzzle[i][j]
        newValue = random.randrange(1, bound+1)
        while newValue == currValue:
            newValue = random.randrange(1, bound+1)
        tempPuzzle[i][j] = newValue
        tempEval = maze_evaluation(tempPuzzle)
        if tempEval <= currEval:
            puzzle = tempPuzzle
            currEval = tempEval
        elif (random.randint(0,100) / 100) < prob:
            puzzle = tempPuzzle
            currEval = tempEval
    if eval:
        print(currEval - originalEval, "better for:  ", x, "  iterations | prob: ",prob)
    return puzzle


print("~~~Problem #1~~~")
puzzle1 = maze_representation(10)
printPuzzle(puzzle1)

print("~~~Problem #2~~~")
puzzle2 = maze_representation(7)
print(maze_evaluation(puzzle2))

print("~~~Problem #3~~~")
puzzle3 = maze_generation(5,3)
printPuzzle(puzzle3)

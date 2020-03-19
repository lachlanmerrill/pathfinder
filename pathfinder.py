map_matrix = [  # Example map matrix. Don't use this for actual implementation because there are so many things wrong
                # with it.
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
    [5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5],
    [5, 0, 5, 5, 0, 5, 0, 5, 5, 0, 5],
    [5, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5],
    [5, 0, 0, 0, 5, 5, 0, 3, 0, 0, 5],
    [5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5],
    [5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5],
    [5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
]

# Const values for where things are in cell tuples
X = 0
Y = 1
COUNT = 2

# Map array boundaries. Set these accordingly for whatever size of map you're working with
ROW_LENGTH = 10
COL_HEIGHT = 10

# Example start cell
start_cell = (1, 1)

# Example goal cell
goal_cell = (5, 7)


def determine(cell, queue):
    # Out of bounds check
    if cell[X] >= ROW_LENGTH or cell[Y] >= COL_HEIGHT or cell[X] < 0 or cell[Y] < 0:
        return False
    # Wall check
    if map_matrix[cell[X]][cell[Y]] == 'X':
        return False
    # Duplicate value check. Makes this O(log(n)) complexity because queue gets exponentially longer. Probably a better
    # way to do it...
    for q in queue:
        if q[X] == cell[X] and q[Y] == cell[Y] and q[COUNT] <= cell[COUNT]:
            return False
    # Cell is valid if the function gets to this point so return true
    return True


def pathfinder(curr, goal):
    # Reformat matrix. This part can be ignored or removed depending on how you format the map
    # Basically I initialized the map_matrix using integers and couldn't be bothered refactoring it so walls are
    # X's. Don't use integers in the map if possible, since they'll mess with the path finding algorithm.
    # Also this implementation overwrites the map so you'll want to find some way to copy it by value to avoid
    # messing it up
    path_matrix = map_matrix[:][:]
    for x in range(0, ROW_LENGTH):
        for y in range(0, COL_HEIGHT):
            if path_matrix[x][y] == 5:
                path_matrix[x][y] = 'X'
            if path_matrix[x][y] == 0:
                path_matrix[x][y] = -1

    # Set goal position and current position
    # Makes code look a little bit nicer by extracting the values from their tuples
    x_goal = goal[0]
    y_goal = goal[1]
    x_position = curr[0]
    y_position = curr[1]

    # Initialize queue for initial loop
    queue = [(x_goal, y_goal, 0)]
    queue_counter = 0  # Current position in the queue
    curr_cell = queue[queue_counter]  # Current cell in the queue
    curr_cell_count = curr_cell[COUNT]  # Current cell's score (steps removed from goal position)

    # Find scores for path - starts at goal position and terminates at start position
    while not (curr_cell[X] == x_position and curr_cell[Y] == y_position):
        # create a list of adjacent cells
        adjacent = [(curr_cell[X] + 1,  curr_cell[Y],       curr_cell_count + 1),
                    (curr_cell[X],      curr_cell[Y] + 1,   curr_cell_count + 1),
                    (curr_cell[X] - 1,  curr_cell[Y],       curr_cell_count + 1),
                    (curr_cell[X],      curr_cell[Y] - 1,   curr_cell_count + 1)]

        # Array comprehension to strip out walls, out of bounds locations and duplicate values
        adjacent = [cell for cell in adjacent if determine(cell, queue)]

        # iterate through each adjacent cell candidate and remove if it is a wall or already has a lower score
        for cell in adjacent:
            # If the cell wasn't removed then append it to the queue
            queue.append(cell)

        # Write current cell score to temp map
        path_matrix[curr_cell[X]][curr_cell[Y]] = curr_cell[COUNT]
        # Move to next cell in queue
        queue_counter += 1
        curr_cell = queue[queue_counter]

        curr_cell_count = curr_cell[COUNT]

    # setup for next loop
    curr_cell = (x_position, y_position) # Initialize current cell at start position
    offset_values = [(1, 0), # Lookup table for direction of movement from lowest score index in adjacent cells list
                     (0, 1),
                     (-1, 0),
                     (0, -1)]

    while not (curr_cell[X] == x_goal and curr_cell[Y] == y_goal):
        # Fetch cells adjacent to current cell
        adjacent = (
            path_matrix[curr_cell[X] + 1][curr_cell[Y]],
            path_matrix[curr_cell[X]][curr_cell[Y] + 1],
            path_matrix[curr_cell[X] - 1][curr_cell[Y]],
            path_matrix[curr_cell[X]][curr_cell[Y] - 1]
        )

        # Set lowest score to be the first adjacent cell if it is an int, or an unreasonably large number otherwise
        lowest_score = adjacent[0] if type(adjacent[0]) is int else len(queue)
        lowest_cell = 0

        # Find lowest scoring adjacent cell's index
        for i in range(0, 4):
            tmp = adjacent[i]
            if tmp == 'X' or tmp == -1 or tmp == 'P':
                continue
            if tmp < lowest_score:
                lowest_score = tmp
                lowest_cell = i

        # Overwrite current cell with a P character to indicate we've pathed through it
        path_matrix[curr_cell[X]][curr_cell[Y]] = 'P'

        # Go to next cell using offsets from offset_values
        curr_cell = (curr_cell[X] + offset_values[lowest_cell][X], curr_cell[Y] + offset_values[lowest_cell][Y])

    path_matrix[curr_cell[X]][curr_cell[Y]] = 'P'

    # Print the matrix in a pretty format
    for row in path_matrix:
        for col in row:
            if col == 'P':
                col = '  ' + '\033[34m' + 'P' + '\033[m'
                print(str(col), end='')
            else:
                print(str(col).rjust(3, ' '), end='')
        print("\n", end='')

print("starting\n")
pathfinder(start_cell, goal_cell)

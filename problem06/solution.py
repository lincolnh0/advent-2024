DIRECTION_LIST = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_next_obstacles(guard_pos, cur_dir, obst_array):
    # Find the closest next obstacle
    for x, y in sorted(obst_array, key=lambda pos: abs(pos[0] - guard_pos[0]) + abs(pos[1] - guard_pos[1])):
        dx = x - guard_pos[0]
        dy = y - guard_pos[1]
        if dx == 0:
            if cur_dir[1] != 0 and (dy / cur_dir[1]) >= 1:
                return x, y
        if dy == 0:
            if cur_dir[0] != 0 and (dx / cur_dir[0]) >= 1:
                return x, y

def solution_p1(input_data: str):
    guard = (0, 0)
    obstacles = []
    for row_index, line in enumerate(input_data.splitlines()):
        for col_index, row in enumerate(list(line)):
            if row == "^":
                guard = (row_index, col_index)
            if row == "#":
                obstacles.append((row_index, col_index))

    direction = DIRECTION_LIST[0]

    next_obstacle = get_next_obstacles(guard, direction, obstacles)

    steps = {(guard, direction)}
    while next_obstacle:
        distance_covered = abs(next_obstacle[0] - guard[0]) + abs(next_obstacle[1] - guard[1]) - 1
        steps = steps | {((guard[0] + i * direction[0], guard[1] + i * direction[1]), direction) for i in range(1, distance_covered + 1)}
        guard = next_obstacle[0] - direction[0], next_obstacle[1] - direction[1]
        direction = DIRECTION_LIST[(DIRECTION_LIST.index(direction) + 1) % len(DIRECTION_LIST)]
        next_obstacle = get_next_obstacles(guard, direction, obstacles)

    # Going out of the map.
    while guard[0] < len(input_data.splitlines()) - 1 and guard[1] < len(input_data.splitlines()) - 1:
        guard = guard[0] + direction[0], guard[1] + direction[1]
        steps = steps | {(guard, direction)}

    return steps

def solution_p2(input_data):
    original_guard_position = (0, 0)
    obstacles = []
    for row_index, line in enumerate(input_data.splitlines()):
        for col_index, row in enumerate(list(line)):
            if row == "^":
                original_guard_position = (row_index, col_index)
            if row == "#":
                obstacles.append((row_index, col_index))

    unaltered_steps_with_directions = solution_p1(input_data)
    valid_new_obstacles = {x[0] for x in unaltered_steps_with_directions}
    valid_new_obstacles.remove(original_guard_position)

    looping_obstacles = []

    for potential_new_obstacle in valid_new_obstacles:
        guard = original_guard_position
        direction = DIRECTION_LIST[0]
        new_obstacles_list = obstacles + [potential_new_obstacle]

        next_obstacle = get_next_obstacles(guard, direction, new_obstacles_list)
        new_start_steps = {(guard, direction)}
        while next_obstacle:
            distance_covered = abs(next_obstacle[0] - guard[0]) + abs(next_obstacle[1] - guard[1]) - 1
            steps_to_walk = {((guard[0] + i * direction[0], guard[1] + i * direction[1]), direction) for i in
                        range(1, distance_covered + 1)}
            if new_start_steps & steps_to_walk:
                looping_obstacles.append(next_obstacle)
                break
            new_start_steps = new_start_steps | steps_to_walk
            guard = next_obstacle[0] - direction[0], next_obstacle[1] - direction[1]
            direction = DIRECTION_LIST[(DIRECTION_LIST.index(direction) + 1) % len(DIRECTION_LIST)]
            next_obstacle = get_next_obstacles(guard, direction, new_obstacles_list)

    print(len(looping_obstacles))
if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#..."

    # print(len({x[0] for x in solution_p1(puzzle_data)}))
    solution_p2(puzzle_data)
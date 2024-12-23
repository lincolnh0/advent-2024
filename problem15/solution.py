import re
from collections import Counter


def format_data(input_data):
    sliced_data = input_data.splitlines()
    empty_index = sliced_data.index("")
    location_data = sliced_data[:empty_index]
    instruction_set = "".join(sliced_data[empty_index:])

    return location_data, instruction_set

def solution_p1(input_data):
    directions_mapping = {
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
        "v": (0, 1),
    }
    location_map, instructions = format_data(input_data)

    block_types = Counter("".join(location_map))
    line_length = len(location_map[0]) + 1

    block_regex = {
        "#": "#",
        ".": r"\.", # Needed to escape the original .
        "@": r"\@",
        "O": "O",
    }

    block_coordinates = {
        block_name: sorted({
            (x.start() % line_length, x.start() // line_length)
            for x in re.finditer(block_regex[block_name], input_data)
        })
        for block_name in block_types
    }

    block_map = {
        coordinates: block_name
        for block_name in block_coordinates
        for coordinates in block_coordinates[block_name]
    }

    guard_position = block_coordinates["@"].pop()

    for instruction in instructions:
        current_direction = directions_mapping[instruction]
        next_tile = next_guard_tile = guard_position[0] + current_direction[0], guard_position[1] + current_direction[1]

        if block_map[next_tile] == "#":
            continue

        if block_map[next_tile] == ".":
            block_map[guard_position] = "."
            guard_position = next_guard_tile
            block_map[guard_position] = "@"
            continue

        while block_map[next_tile] == "O":
            next_tile = next_tile[0] + current_direction[0], next_tile[1] + current_direction[1]

            if block_map[next_tile] == ".":
                block_map[next_tile] = "O"
                block_map[guard_position] = "."
                guard_position = next_guard_tile
                block_map[guard_position] = "@"
                break

    for i in range(8):
        line = ""
        for j in range(8):
            line += block_map[(j, i)]

    gps_coordinates_sum = sum(100 * coord[1] + coord[0] for coord, value in block_map.items() if value == "O")
    return gps_coordinates_sum


def solution_p2(input_data):
    pass


if __name__ == "__main__":

    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    small_example_data = "########\n#..O.O.#\n##@.O..#\n#...O..#\n#.#.O..#\n#...O..#\n#......#\n########\n\n<^^>>>vv<v>>v<<"
    large_example_data = "##########\n#..O..O.O#\n#......O.#\n#.OO..O.O#\n#..O@..O.#\n#O#..O...#\n#O..O..O.#\n#.OO.O.OO#\n#....O...#\n##########\n\n<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\nvvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\nv^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"

    print(solution_p1(puzzle_data))
    solution_p2(small_example_data)
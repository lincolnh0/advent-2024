import re


def recursive_neighbour_finding(
    current_height, current_coordinate, height_coordinates, trails=None
):
    if not trails:
        trails = []

    distance_vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    possible_coordinates = {
        (x + current_coordinate[0], y + current_coordinate[1])
        for x, y in distance_vectors
    }
    trails += [current_coordinate]

    # Base case: Current height is 8.
    if current_height == 8:
        return height_coordinates[9] & possible_coordinates

    # Recursive case: Filter down possible coordinates and ascend
    output = set()
    for x in height_coordinates[current_height + 1] & possible_coordinates:
        output = output | (
            recursive_neighbour_finding(
                current_height + 1, x, height_coordinates, trails
            )
            or set()
        )

    return output


def solution_p1(input_data):
    trail_map = [[int(y) for y in x] for x in input_data.splitlines()]
    line_length = len(trail_map) + 1

    height_coordinates = {
        height: {
            (x.start() // line_length, x.start() % line_length)
            for x in re.finditer(str(height), input_data)
        }
        for height in range(10)
    }
    return sum(
        [
            len(recursive_neighbour_finding(0, x, height_coordinates))
            for x in height_coordinates[0]
        ]
    )


def recursive_neighbour_finding_p2(
    current_height, current_coordinate, height_coordinates
):
    distance_vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    possible_coordinates = {
        (x + current_coordinate[0], y + current_coordinate[1])
        for x, y in distance_vectors
    }

    # Base case: Current height is 8.
    if current_height == 8:
        return len(height_coordinates[9] & possible_coordinates)

    # Recursive case: Filter down possible coordinates and ascend
    return sum(
        [
            recursive_neighbour_finding_p2(current_height + 1, x, height_coordinates)
            for x in possible_coordinates & height_coordinates[current_height + 1]
        ]
    )


def solution_p2(input_data):
    trail_map = [[int(y) for y in x] for x in input_data.splitlines()]
    line_length = len(trail_map) + 1

    height_coordinates = {
        height: {
            (x.start() // line_length, x.start() % line_length)
            for x in re.finditer(str(height), input_data)
        }
        for height in range(10)
    }
    return sum(
        [
            recursive_neighbour_finding_p2(0, x, height_coordinates)
            for x in height_coordinates[0]
        ]
    )


if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = (
        "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"
    )

    print(solution_p1(puzzle_data))
    print(solution_p2(puzzle_data))

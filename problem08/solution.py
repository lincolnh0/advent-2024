import re
from collections import Counter


def solution_p1(input_data):
    distinct_channels = Counter([y for x in input_data.splitlines() for y in x if y != "."])
    roof_map = [[y for y in x] for x in input_data.splitlines()]

    line_length = len(roof_map) + 1
    antennas_coordinates = {
        channel: ([(x.start() // line_length, x.start() % line_length) for x in re.finditer(channel, input_data)])
        for channel in distinct_channels
    }

    antinodes = set()

    # Apply vector transformation to each of the pairs of antennas.
    for channel, antennas in antennas_coordinates.items():
        for first_antenna in antennas:
            for second_antenna in [x for x in antennas if first_antenna != x]:
                vector_1 = (first_antenna[0] - second_antenna[0], first_antenna[1] - second_antenna[1])
                vector_2 = (second_antenna[0] - first_antenna[0], second_antenna[1] - first_antenna[1])

                antinodes = antinodes | {(first_antenna[0] + vector_1[0], first_antenna[1] + vector_1[1])} | {
                    (second_antenna[0] + vector_2[0], second_antenna[1] + vector_2[1])}

    return len({x for x in antinodes if 0 <= x[0] < len(roof_map) and 0 <= x[1] < len(roof_map)})


def solution_p2(input_data):
    distinct_channels = Counter([y for x in input_data.splitlines() for y in x if y != "."])
    roof_map = [[y for y in x] for x in input_data.splitlines()]

    line_length = len(roof_map) + 1
    antennas_coordinates = {
        channel: ([(x.start() // line_length, x.start() % line_length) for x in re.finditer(channel, input_data)])
        for channel in distinct_channels
    }

    # Initialise with antennas coordinates
    antinodes = {y for coordinates in antennas_coordinates.values() for y in coordinates}

    for channel, antennas in antennas_coordinates.items():
        for first_antenna in antennas:
            for second_antenna in [x for x in antennas if first_antenna != x]:
                vector_1 = (first_antenna[0] - second_antenna[0], first_antenna[1] - second_antenna[1])
                vector_2 = (second_antenna[0] - first_antenna[0], second_antenna[1] - first_antenna[1])

                # Lazy loop to repeat until out of bounds, filter later.
                antinodes = antinodes | {
                    (first_antenna[0] + vector_1[0] * x, first_antenna[1] + vector_1[1] * x)
                    for x in range(1, len(roof_map))
                } | {
                    (second_antenna[0] + vector_2[0] * x, second_antenna[1] + vector_2[1] * x)
                    for x in range(1, len(roof_map))
                }

    return len({x for x in antinodes if 0 <= x[0] < len(roof_map) and 0 <= x[1] < len(roof_map)})


if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "............\n........0...\n.....0......\n.......0....\n....0.......\n......A.....\n............\n............\n........A...\n.........A..\n............\n............"

    print("P1 answer:", solution_p1(puzzle_data))
    print("P2 answer:", solution_p2(puzzle_data))

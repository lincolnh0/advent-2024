import re
from collections import Counter
from functools import reduce
from operator import mul
from time import sleep


def solution_p1(input_data, width, height, cycles):
    patrol_position = Counter()

    for patrol_data in input_data.splitlines():
        position_regex = r"p=(.*)\s"
        velocity_regex = r"v=(.*)"

        position_x, position_y = (
            int(x) for x in re.findall(position_regex, patrol_data).pop().split(",")
        )
        velocity_x, velocity_y = (
            int(x) for x in re.findall(velocity_regex, patrol_data).pop().split(",")
        )

        final_position = (
            (position_x + cycles * velocity_x) % width,
            (position_y + cycles * velocity_y) % height,
        )

        height_midpoint = (height - 1) / 2
        width_midpoint = (width - 1) / 2

        if final_position[0] != width_midpoint and final_position[1] != height_midpoint:
            quadrant = (
                int(final_position[0] > width_midpoint),
                int(final_position[1] > height_midpoint),
            )

            patrol_position[quadrant] += 1

    return reduce(mul, patrol_position.values())


def solution_p2(input_data, width, height):

    positions = []
    velocities = []
    for patrol_data in input_data.splitlines():
        position_regex = r"p=(.*)\s"
        velocity_regex = r"v=(.*)"

        position_x, position_y = (
            int(x) for x in re.findall(position_regex, patrol_data).pop().split(",")
        )
        velocity_x, velocity_y = (
            int(x) for x in re.findall(velocity_regex, patrol_data).pop().split(",")
        )

        positions.append((position_x, position_y))
        velocities.append((velocity_x, velocity_y))

    counter = 1070
    max_unique_coordinates = 0
    while True:
        patrol_coordinates = set()
        counter += 1
        for (position_x, position_y), (velocity_x, velocity_y) in zip(positions, velocities):
            patrol_coordinates.add(((position_x + velocity_x * counter) % width, (position_y + velocity_y * counter) % height))

        patrol_map = []
        for i in range(height):
            line = ""
            for j in range(width):
                if not {(j, i)} & patrol_coordinates:
                    line += " "
                else:
                    line += "x"
            patrol_map.append(line)
        if len(patrol_coordinates) > max_unique_coordinates:
            max_unique_coordinates = len(patrol_coordinates)
            print(*patrol_map, sep="\n")
            print(f"\nCounter {counter}")


if __name__ == "__main__":

    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "p=0,4 v=3,-3\np=6,3 v=-1,-3\np=10,3 v=-1,2\np=2,0 v=2,-1\np=0,0 v=1,3\np=3,0 v=-2,-2\np=7,6 v=-1,-3\np=3,0 v=-1,-2\np=9,3 v=2,3\np=7,3 v=-1,2\np=2,4 v=2,-3\np=9,5 v=-3,-3"
    single_data = "p=2,4 v=2,-3"
    print(solution_p1(puzzle_data, 101, 103, 100))
    solution_p2(puzzle_data, 101, 103)

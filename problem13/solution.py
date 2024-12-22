import re
from platform import machine
from shutil import make_archive


def format_data(input_data):
    individual_lines = input_data.splitlines()
    raw_input_groups = [
        (
            individual_lines[index * 4],
            individual_lines[index * 4 + 1],
            individual_lines[index * 4 + 2],
        )
        for index in range(len(individual_lines) // 4 + 1)
    ]

    control_regex = r"\+(\d*)"
    position_regex = r"=(\d*)"

    input_groups = [
        {
            "A": tuple(int(val) for val in re.findall(control_regex, x)),
            "B": tuple(int(val) for val in re.findall(control_regex, y)),
            "Destination": tuple(int(val) for val in re.findall(position_regex, z)),
        }
        for x, y, z in raw_input_groups
    ]

    return input_groups


def solution_p1(input_data):
    formatted_data = format_data(input_data)

    running_total = 0
    for machine in formatted_data:
        valid_tokens = []
        for button_a in range(101):
            for button_b in range(101):
                combination_coordinates = (
                    button_a * machine["A"][0] + button_b * machine["B"][0],
                    button_a * machine["A"][1] + button_b * machine["B"][1],
                )

                if combination_coordinates == machine["Destination"]:
                    valid_tokens.append(button_a * 3 + button_b)

        running_total += min(valid_tokens, default=0)

    return running_total

class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplementedError
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Coordinate):
            raise NotImplementedError
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Coordinate(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __divmod__(self, other):
        closest_quotient = min(self.x // other.x, self.y // other.y)
        return closest_quotient, Coordinate(self.x - other.x * closest_quotient, self.y - other.y  * closest_quotient)


    def __repr__(self):
        return f"Coordinates({self.x}, {self.y})"


def solution_p2(input_data):
    formatted_data = [
        {
            "A": Coordinate(*x["A"]),
            "B": Coordinate(*x["B"]),
            "Destination": Coordinate(
                10000000000000 + x["Destination"][0],
                10000000000000 + x["Destination"][1],
            ),
        }
        for x in format_data(input_data)
    ]

    running_total = 0

    for machine in formatted_data:
        button_b = (machine["A"].x * machine["Destination"].y - machine["Destination"].x * machine["A"].y) / (machine["A"].x * machine["B"].y - machine["B"].x * machine["A"].y)
        button_a = (machine["Destination"].x - button_b * machine["B"].x) / machine["A"].x

        if button_a.is_integer() and button_b.is_integer():
            running_total += 3 * int(button_a) + int(button_b)

    return running_total


if __name__ == "__main__":

    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "Button A: X+94, Y+34\nButton B: X+22, Y+67\nPrize: X=8400, Y=5400\n\nButton A: X+26, Y+66\nButton B: X+67, Y+21\nPrize: X=12748, Y=12176\n\nButton A: X+17, Y+86\nButton B: X+84, Y+37\nPrize: X=7870, Y=6450\n\nButton A: X+69, Y+23\nButton B: X+27, Y+71\nPrize: X=18641, Y=10279"

    print(solution_p1(puzzle_data))
    print(solution_p2(puzzle_data))

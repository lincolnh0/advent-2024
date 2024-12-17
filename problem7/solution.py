import re

def clean_data(input_data):
    line_split_regex = r"(\d*)\: (.*)"
    matches = re.finditer(line_split_regex, input_data)
    return [
        (int(match.group(1)), [int(x) for x in match.group(2).split(" ")])
        for match in matches
    ]

def get_possible_operator_p1(target, current, numbers):
    # Base case: There is only one number.
    if len(numbers) == 1:
        return current + numbers[0] == target or current * numbers[0] == target
    # Recursive case: There are more than one number
    return get_possible_operator_p1(target, current + numbers[0], numbers[1:]) or get_possible_operator_p1(target, current * numbers[0], numbers[1:])


def solution_p1(input_data):
    running_total = 0
    for row_total, row_components in input_data:
        is_possible = get_possible_operator_p1(row_total, row_components[0], row_components[1:])
        if is_possible:
            running_total += row_total

    return running_total

def get_possible_operator_p2(target, current, numbers):
    # Base case: There is only one number.
    if len(numbers) == 1:
        return current + numbers[0] == target or current * numbers[0] == target or str(current) + str(numbers[0]) == str(target)
    # Recursive case: There are more than one number
    return get_possible_operator_p2(target, current + numbers[0], numbers[1:]) or get_possible_operator_p2(target, current * numbers[0], numbers[1:]) or get_possible_operator_p2(target, int(str(current) + str(numbers[0])), numbers[1:])


def solution_p2(input_data):
    running_total = 0
    for row_total, row_components in input_data:
        is_possible = get_possible_operator_p2(row_total, row_components[0], row_components[1:])
        if is_possible:
            running_total += row_total

    return running_total


if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20"

    print(solution_p1(clean_data(puzzle_data)))
    print(solution_p2(clean_data(puzzle_data)))
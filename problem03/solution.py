import re


def solution_p1(input_data):
    regex = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.finditer(regex, input_data, re.MULTILINE)

    total_sum = sum([
        int(match.group(1)) * int(match.group(2))
        for match in matches
    ])

    return total_sum


def solution_p2(input_data, enabled=True):
    disable_regex = r"don\'t\(\)"
    enable_regex = r"do\(\)"

    # Find next opposite marker.
    disable_match = re.search(disable_regex, input_data, re.MULTILINE)
    enable_match = re.search(enable_regex, input_data, re.MULTILINE)

    # Base case, where neither of the opposite marker is found.
    if enabled:
        if not disable_match:
            return solution_p1(input_data)

    else:
        if not enable_match:
            return 0

    # Find the next opposite marker and return sum between
    if enabled:
        return (
                solution_p1(input_data[:disable_match.start()]) +
                solution_p2(input_data[disable_match.end():], enabled=False)
        )

    else:
        return solution_p2(input_data[enable_match.end():], enabled=True)


if __name__ == '__main__':
    example_data_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    example_data_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    with open('./input.txt') as f:
        puzzle_data = f.read()

    print(solution_p2(puzzle_data))

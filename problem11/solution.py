from collections import Counter


def solution_p1(input_data):
    digits = [int(x) for x in input_data.split(" ")]

    for i in range(25):
        new_arrangement = []
        for digit in digits:
            if digit == 0:
                new_arrangement.append(1)
            elif len(str(digit)) % 2 == 0:
                new_arrangement.extend([int(str(digit)[:len(str(digit)) // 2]), int(str(digit)[len(str(digit)) // 2:])])
            else:
                new_arrangement.append(digit * 2024)

        digits = new_arrangement

    return len(digits)


def blink_change(digit):

    if digit == 0:
        yield 1

    elif len(str(digit)) % 2 == 0:
        yield int(str(digit)[:len(str(digit)) // 2])
        yield int(str(digit)[len(str(digit)) // 2:])
    else:
        yield digit * 2024


def solution_p2(counts, times):
    digits = Counter([int(x) for x in counts.split(" ")])
    for _ in range(times):
        new_counter = Counter()
        for stone, occurrences in digits.items():
            for newstone in blink_change(stone):
                new_counter[newstone] += occurrences
        digits = new_counter
    return sum(digits.values())


if __name__ == "__main__":

    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "125 17"

    print(solution_p1(puzzle_data))
    print(solution_p2(puzzle_data, 75))
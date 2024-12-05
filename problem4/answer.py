import numpy as np
import re

def solution_p1(input_data):

    # Transpose matrix and look for both forward and backward spelled XMAS
    horizontal_matrix = np.array([[y for y in x.strip()] for x in input_data.splitlines() if x.strip()])
    vertical_matrix = horizontal_matrix.transpose()

    # Rotate the matrix 45 degrees both way and perform the same check
    rotated_matrix = []
    height, width = horizontal_matrix.shape
    counter = 0
    while counter <= height + width:
        diagonal_row = []
        reversed_row = []
        for i in range(height):
            for j in range(width):
                if (i + j) == counter:
                    diagonal_row.append(str(horizontal_matrix[i][j]))
                    reversed_row.append(str(horizontal_matrix[height - i - 1][j]))
        counter += 1
        rotated_matrix.append(diagonal_row)
        rotated_matrix.append(reversed_row)

    joined_horizontal_matrix = ["".join(x) for x in horizontal_matrix]
    joined_vertical_matrix = ["".join(x) for x in vertical_matrix]
    joined_rotated_matrix = ["".join(x) for x in rotated_matrix]

    horizontal_occurrences = sum([x.count("XMAS") + x.count("SAMX") for x in joined_horizontal_matrix])
    vertical_occurrences = sum([x.count("XMAS") + x.count("SAMX") for x in joined_vertical_matrix])
    rotated_occurrences = sum([x.count("XMAS") + x.count("SAMX") for x in joined_rotated_matrix])

    return sum([horizontal_occurrences, vertical_occurrences, rotated_occurrences])


def solution_2(input_data):
    matrix = [x.strip() for x in input_data.splitlines() if x.strip()]

    # Looking for A's 1 character inwards
    a_regex = r"A"
    counter = 0
    pattern = ["MMSS", "SSMM", "MSMS", "SMSM"]
    for i in range(1, len(matrix) - 1):
        row_text = matrix[i][1:-1]

        a_occurrences = re.finditer(a_regex, row_text)

        start_positions = [x.start() for x in a_occurrences]

        for start_pos in start_positions:
            top_check_pos1, top_check_pos2 = matrix[i - 1][start_pos], matrix[i - 1][start_pos + 2]
            bottom_check_pos1, bottom_check_pos2 = matrix[i + 1][start_pos], matrix[i + 1][start_pos + 2]

            check_pattern = top_check_pos1 + top_check_pos2 + bottom_check_pos1 + bottom_check_pos2

            if check_pattern in pattern:
                counter += 1



    return counter



if __name__ == "__main__":
    example_data = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """

    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    print(solution_p1(puzzle_data))
    print(solution_2(puzzle_data))

import itertools

def solution_p1(input_data):
    file_blocks_lengths = {
        int(x / 2): int(input_data[x])
        for x in range(0, len(input_data), 2)
    }

    file_blocks_start = {
        int(x / 2): sum([int(y) for y in input_data[:x]])
        for x in range(0, len(input_data), 2)
    }

    space_blocks = {
        sum([int(y) for y in input_data[:x]]): int(input_data[x])
        for x in range(1, len(input_data), 2)
    }

    spaces = [y for start, length in space_blocks.items() for y in range(start, start + length)]

    # Total number of blocks after rearrangement
    total_block_length = sum([x for x in file_blocks_lengths.values()])

    # First run of checksum, only adding up to the minimum required number of blocks.
    checksum = 0
    for file_id in file_blocks_start:
        checksum += sum([
            file_id * x for x in range(
                file_blocks_start[file_id], min(total_block_length, file_blocks_start[file_id] + file_blocks_lengths[file_id])
            )
        ])

    # Perform space replacement.
    reverse_file_blocks = itertools.chain(*[
        [x] * file_blocks_lengths[x] for x in reversed(file_blocks_lengths)
    ])
    checksum += sum([
        file_id * index
        for file_id, index in list(zip(list(reverse_file_blocks), spaces)) if index < total_block_length
    ])

    return checksum

def solution_p2(input_data):
    file_blocks_lengths = {
        int(x / 2): int(input_data[x])
        for x in range(0, len(input_data), 2)
    }

    file_blocks_start = {
        int(x / 2): sum([int(y) for y in input_data[:x]])
        for x in range(0, len(input_data), 2)
    }

    space_blocks = {
        sum([int(y) for y in input_data[:x]]): int(input_data[x])
        for x in range(1, len(input_data), 2)
    }

    # Only fill spaces that are left of the current file.
    for file_id, block_length in reversed(file_blocks_lengths.items()):
        for space_index, space_length in sorted(space_blocks.items()):
            if block_length <= space_length and space_index < file_blocks_start[file_id]:
                file_blocks_start[file_id] = space_index
                space_blocks.pop(space_index)
                if space_length - block_length > 0:
                    space_blocks[space_index + block_length] = space_length - block_length
                break

    checksum = 0
    for file_id in file_blocks_start:
        checksum += sum([file_id * x for x in range(file_blocks_start[file_id], file_blocks_start[file_id] + file_blocks_lengths[file_id])])

    return checksum

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    example_data = "2333133121414131402"

    # print(solution_p1(puzzle_data))

    print(solution_p2(puzzle_data))

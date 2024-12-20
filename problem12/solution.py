from collections import Counter, defaultdict
import re


def recursive_find_region(
    current_tile: tuple[int, int], neighbours: dict[tuple, set], discovered_tiles: set
):

    # Base case: All tiles discovered
    if neighbours[current_tile].issubset(discovered_tiles):
        return discovered_tiles | {current_tile}

    # Recursive case: Append current tiles to discovered and continue exploring
    depth_discovered_tiles = discovered_tiles | {current_tile}
    for current_neighbour in neighbours[current_tile].difference(
        depth_discovered_tiles, {current_tile}
    ):
        depth_discovered_tiles = depth_discovered_tiles | recursive_find_region(
            current_neighbour, neighbours, depth_discovered_tiles
        )

    return depth_discovered_tiles


def solution_p1(input_data):
    plot_area = Counter([y for x in input_data.splitlines() for y in x])

    line_length = len(input_data.splitlines()) + 1
    land_coordinates = {
        region_name: {
            (x.start() // line_length, x.start() % line_length)
            for x in re.finditer(region_name, input_data)
        }
        for region_name in plot_area
    }

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    running_costs = 0

    for region_name, region_coordinates in land_coordinates.items():
        neighbours = {
            (x1, y1): {(x1 + x2, y1 + y2) for x2, y2 in directions} & region_coordinates
            for x1, y1 in region_coordinates
        }
        regions = Counter(
            [frozenset(recursive_find_region(x, neighbours, set())) for x in neighbours]
        )
        for coordinates, area in regions.items():
            perimeter = sum(
                [4 - len(neighbours[current_tile]) for current_tile in coordinates]
            )
            running_costs += perimeter * area

    return running_costs

def recursive_find_edge(coordinates, direction, current_tile):
    next_tile = current_tile[0] + direction[0], current_tile[1] + direction[1]

    if next_tile not in coordinates:
        return {current_tile}

    return recursive_find_edge(coordinates, direction, next_tile) | {current_tile}

def count_edges(edge_neighbours, directions):
    straight_edges = 0
    visited = set()

    for current_tile in edge_neighbours:
        if current_tile in visited:
            continue

        for direction in directions:
            nx, ny = current_tile[0] + direction[0], current_tile[1] + direction[1]
            if (nx, ny) in edge_neighbours and (nx, ny) not in visited:
                straight_edges += 1
                visited.add((nx, ny))

    return straight_edges


def solution_p2(input_data):
    plot_area = Counter([y for x in input_data.splitlines() for y in x])

    line_length = len(input_data.splitlines()) + 1
    land_coordinates = {
        region_name: {
            (x.start() // line_length, x.start() % line_length)
            for x in re.finditer(region_name, input_data)
        }
        for region_name in plot_area
    }

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    running_costs = 0

    for region_name, region_coordinates in land_coordinates.items():
        neighbours = {
            (x1, y1): {(x1 + x2, y1 + y2) for x2, y2 in directions} & region_coordinates
            for x1, y1 in region_coordinates
        }
        non_edge_tiles = {k for k, v in neighbours.items() if len(v) == 4}
        edge_neighbours = {
            k: v.difference(non_edge_tiles) for k, v in neighbours.items() if len(v) < 4
        }

        regions = Counter(
            [frozenset(recursive_find_region(x, neighbours, set())) for x in neighbours]
        )
        for coordinates, area in regions.items():
            perimeter = count_edges(edge_neighbours, directions)
            running_costs += perimeter * area
            print(f"{region_name=} {perimeter=} {area=}")

    return running_costs

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        puzzle_data = f.read()

    short_data = "AAAA\nBBCD\nBBCC\nEEEC"
    short_data2 = "AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA"
    example_data = "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"

    # print(solution_p1(short_data2))
    print(solution_p2(short_data))

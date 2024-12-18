import math
from collections import defaultdict


def solution_p1(rules, orders):

    formatted_rules = [x.strip() for x in rules.splitlines() if x.strip()]

    rules_dict = defaultdict(list)

    for before, after in [x.split("|") for x in formatted_rules]:
        rules_dict[after].append(before)

    formatted_orders = [x.strip() for x in orders.splitlines() if x.strip()]

    invalid_orders = []
    for order in formatted_orders:
        for index, value in enumerate(order.split(",")):
            if set(rules_dict[value]) & set(order.split(",")[index:]):
                invalid_orders.append(order)
                break
    middle_pages_sum = 0
    for order in (set(formatted_orders) - set(invalid_orders)):
        split_order = order.split(",")
        middle_pages_sum += int(split_order[math.floor(len(split_order) / 2)])

    return middle_pages_sum

def solution_p2(rules, orders):

    formatted_rules = [x.strip() for x in rules.splitlines() if x.strip()]
    rules_dict = defaultdict(set)
    for before, after in [x.split("|") for x in formatted_rules]:
        rules_dict[after].add(before)

    formatted_orders = [x.strip() for x in orders.splitlines() if x.strip()]

    invalid_orders = []
    for order in formatted_orders:
        for index, value in enumerate(order.split(",")):
            if set(rules_dict[value]) & set(order.split(",")[index:]):
                invalid_orders.append(order)
                break

    middle_pages_sum = 0

    for invalid_order in invalid_orders:
        rearranged_order = []
        numbers = set(invalid_order.split(","))
        while numbers:
            elements_in_front = set.union(*[rules_dict[value] for value in numbers]) & set(numbers)
            rearranged_order.append(int(next(iter(numbers.difference(elements_in_front)))))
            numbers = elements_in_front


        middle_pages_sum += int(list(reversed(rearranged_order))[math.floor(len(rearranged_order) / 2)])

    return middle_pages_sum

if __name__ == "__main__":
    example_data_rules = """
            47|53
            97|13
            97|61
            97|47
            75|29
            61|13
            75|53
            29|13
            97|29
            53|29
            61|53
            97|53
            61|29
            47|13
            75|47
            97|75
            47|61
            75|61
            47|29
            75|13
            53|13
            """
    example_data_orders = """75,47,61,53,29
                             97,61,53,29,13
                             75,29,13
                             75,97,47,61,53
                             61,13,29
                             97,13,75,29,47"""

    with open("input_orders.txt", "r") as f:
        puzzle_data_orders = f.read()

    with open("./input_rules.txt", "r") as f:
        puzzle_data_rules = f.read()

    example_rules = "47|53\n97|13\n97|61\n97|47\n75|29\n61|13\n75|53\n29|13\n97|29\n53|29\n61|53\n97|53\n61|29\n47|13\n75|47\n97|75\n47|61\n75|61\n47|29\n75|13\n53|13"
    example_orders = "75,47,61,53,29\n97,61,53,29,13\n75,29,13\n75,97,47,61,53\n61,13,29\n97,13,75,29,47"

    print(solution_p1(puzzle_data_rules, puzzle_data_orders))
    print(solution_p2(puzzle_data_rules, puzzle_data_orders))



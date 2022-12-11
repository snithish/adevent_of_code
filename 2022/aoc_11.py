import operator
from dataclasses import dataclass
from functools import reduce
from typing import List, Callable, Dict

MonkeyId = int
Item = int
Items = List[Item]


@dataclass
class Monkey:
    id: MonkeyId
    items: Items
    mapper: Callable[[Item], Item]
    test: int
    outcomes: Dict[bool, MonkeyId]
    total_inspected: int = 0

    def _inspect(self) -> Items:
        self.total_inspected += len(self.items)
        return [self.mapper(i) for i in self.items]

    def throw(self, relief: Callable[[Item], Item]) -> Dict[MonkeyId, Items]:
        new_worry_level = self._inspect()
        wl_after_relief = [relief(wl) for wl in new_worry_level]
        # wl_after_relief = new_worry_level
        sending: Dict[MonkeyId, Items] = {}
        for wl in wl_after_relief:
            test_outcome = (wl % self.test) == 0
            dst_monkey: MonkeyId = self.outcomes[test_outcome]
            items_to_send = sending.get(dst_monkey, [])
            items_to_send.append(wl)
            sending[dst_monkey] = items_to_send
        self.items = []  # after throwing no more items
        return sending

    def catch(self, new_items: Items):
        self.items.extend(new_items)


# Monkey 0:
# Starting items: 61
# Operation: new = old * 11
# Test: divisible by 5
# If true: throw to monkey 7
# If false: throw to monkey 4

def construct_init_state(_: List[str]) -> Dict[MonkeyId, Monkey]:
    monkey0 = Monkey(0, [61], lambda x: x * 11, 5, {True: 7, False: 4})
    monkey1 = Monkey(1, [76, 92, 53, 93, 79, 86, 81], lambda x: x + 4, 2, {True: 2, False: 6})
    monkey2 = Monkey(2, [91, 99], lambda x: x * 19, 13, {True: 5, False: 0})
    monkey3 = Monkey(3, [58, 67, 66], lambda x: x * x, 7, {True: 6, False: 1})
    monkey4 = Monkey(4, [94, 54, 62, 73], lambda x: x + 1, 19, {True: 3, False: 7})
    monkey5 = Monkey(5, [59, 95, 51, 58, 58], lambda x: x + 3, 11, {True: 0, False: 4})
    monkey6 = Monkey(6, [87, 69, 92, 56, 91, 93, 88, 73], lambda x: x + 8, 3, {True: 5, False: 2})
    monkey7 = Monkey(7, [71, 57, 86, 67, 96, 95], lambda x: x + 7, 17, {True: 3, False: 1})
    monkeys = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]
    return {m.id: m for m in monkeys}


def handle_round(state: Dict[MonkeyId, Monkey], relief: Callable[[Item], Item]):
    for mid in range(0, len(state.keys())):
        current_monkey = state[mid]
        throw_map = current_monkey.throw(relief)
        for dmid, thrown_items in throw_map.items():
            state[dmid].catch(thrown_items)
    return state


def main(init_actions: List[str], rounds: int, part: str):
    state = construct_init_state(init_actions)
    relief = lambda x: x // 3
    if part == "B":
        common_multiple = reduce(operator.mul, [m.test for m in state.values()])
        relief = lambda x: x % common_multiple
    for _ in range(0, rounds):
        state = handle_round(state, relief)
    sorted_active = sorted([m.total_inspected for m in state.values()], reverse=True)
    print(sorted_active[0] * sorted_active[1])


if __name__ == '__main__':
    inputs = []
    with open("./data/aoc_11.txt", mode="r", newline="\n") as f:
        inputs = f.readlines()
    main(inputs, 20, "A")
    main(inputs, 10000, "B")

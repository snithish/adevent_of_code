from unittest import TestCase
from aoc_11 import Monkey, handle_round


class Test(TestCase):
    def test_handle_round(self):
        monkey0 = Monkey(0, [79, 98], lambda x: x * 19, 23, {True: 2, False: 3})
        monkey1 = Monkey(1, [54, 65, 75, 74], lambda x: x + 6, 19, {True: 2, False: 0})
        monkey2 = Monkey(2, [79, 60, 97], lambda x: x * x, 13, {True: 1, False: 3})
        monkey3 = Monkey(3, [74], lambda x: x + 3, 17, {True: 0, False: 1})

        state = {m.id: m for m in [monkey0, monkey1, monkey2, monkey3]}

        for i in range(0, 20):
            state = handle_round(state)
            print(f"Round {i}: {[(i, m.items, m.total_inspected) for i, m in state.items()]}")

        sorted_active = sorted([m.total_inspected for m in state.values()], reverse=True)
        print(sorted_active[0] * sorted_active[1])

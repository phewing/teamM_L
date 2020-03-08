from __future__ import annotations

import re
from enum import Enum
from typing import List


pattern = re.compile(r"((?:self)|(?:(?:identical )?twin)|(?:sibling(?: \d+)?)|(?:\bfather\b)|(?:grandmother)|"
                     r"(?:grandfather)|(?:paternal)|(?:\bmate\b(?: \d+)?)|(?:child(?: \d+)?)|(?:mother)|(?:maternal))+",
                     re.IGNORECASE)


class StepDirection(Enum):
    FATHER = 1
    MOTHER = 2
    SIBLING = 3
    CHILD = 4
    MATE = 5


class Step(object):
    direction: StepDirection
    index: int

    def __init__(self, direction: StepDirection, index: int = None):
        self.direction = direction
        self.index = index

        if index is None and direction == StepDirection.SIBLING or direction == StepDirection.CHILD:
            self.index = 1

    def __str__(self):
        return f"{self.direction} {self.index}"

    def __eq__(self, other: Step) -> bool:
        return self.direction == other.direction and self.index == other.index


class StepSequence(object):
    items: List[Step]

    def __init__(self, items: List[Step]=None):
        if items is None:
            items = []
        self.items = items

    def __str__(self):
        return ", ".join([str(item) for item in self.items])

    def add_item(self, item: Step):
        self.items.append(item)

    def __eq__(self, other: StepSequence) -> bool:
        if len(self.items) != len(other.items):
            return False

        for i in range(len(self.items)):
            if self.items[i] != other.items[i]:
                return False

        return True


def parse_relationship_text(txt: str) -> StepSequence:
    parts = [part.lower() for part in pattern.findall(txt)]

    sequence = StepSequence()

    while True:
        if len(parts) == 0:
            break

        front = parts.pop(0)

        spl = front.split(" ")

        if len(spl) == 1 or front == "identical twin":
            # With no index
            if front == "self":
                pass
            elif front == "twin" or front == "identical twin":
                pass
            elif front == "mate":
                sequence.add_item(Step(StepDirection.MATE))
            elif front == "maternal" or front == "mother" or front == "grandmother":
                sequence.add_item(Step(StepDirection.MOTHER))
            elif front == "paternal" or front == "father" or front == "grandfather":
                sequence.add_item(Step(StepDirection.FATHER))
            elif front == "sibling":
                sequence.add_item(Step(StepDirection.SIBLING))
            elif front == "child":
                sequence.add_item(Step(StepDirection.CHILD))
            else:
                raise ValueError(front)
        elif len(spl) == 2:
            # With index
            index = int(spl[1])
            front = spl[0]

            if front == "sibling":
                sequence.add_item(Step(StepDirection.SIBLING, index))
            elif front == "child":
                sequence.add_item(Step(StepDirection.CHILD, index))
            elif front == "mate":
                sequence.add_item(Step(StepDirection.MATE, index))
            else:
                raise ValueError(front)
        else:
            raise ValueError(front)

    return sequence



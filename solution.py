# ENGINEERING VERIFICATION AND VALIDATION SIGN-OFF
# Engineer Name:
# Aws Ibraheem
# By signing my name above, I confirm that I have reviewed this
# implementation as a software engineer would before approving work
# for release. I verified it against the stated requirements, validated
# its behavior with tests, and evaluated whether it preserves the
# required data-structure invariants.
#
# Based on the evidence I collected, I am willing to attach my name
# to this solution and sign off on its submission. I accept professional
# responsibility for the complete solution, including any portions
# developed with generative AI assistance.

"""
CSE 331
Project 4
starter.py
"""

from __future__ import annotations

from typing import List, Tuple, TypeVar

T = TypeVar("T")


class CircularDeque:
    """
    Circular double-ended queue backed by a Python list.
    """

    __slots__ = ["capacity", "size", "queue", "front", "back"]

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4) -> None:
        """
        DO NOT MODIFY
        """
        if data is None and front != 0:
            data = ["Start"]
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """DO NOT MODIFY"""
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append("(F)")
            elif i == self.back:
                str_list.append("(B)")
            if i < self.capacity - 1:
                str_list.append(",")
        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    def __len__(self) -> int:
        """Return the number of elements in the deque."""
        return self.size

    def is_empty(self) -> bool:
        """Return True if the deque is empty, otherwise False."""
        return self.size == 0

    def front_element(self) -> T:
        """Return the front element without removing it."""
        if self.is_empty():
            return None

        return self.queue[self.front]

    def back_element(self) -> T:
        """Return the back element without removing it."""
        if self.is_empty():
            return None

        return self.queue[self.back]

    def enqueue(self, value: T, front: bool = True) -> None:
        """Insert a value at the front or back of the deque."""
        if self.is_empty():
            self.front = 0
            self.back = 0
            self.queue[0] = value

        elif front:
            self.front = (self.front - 1) % self.capacity
            self.queue[self.front] = value

        else:
            self.back = (self.back + 1) % self.capacity
            self.queue[self.back] = value

        self.size += 1

        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """Remove and return the front or back element of the deque."""
        if self.is_empty():
            return None

        if front:
            value = self.queue[self.front]
        else:
            value = self.queue[self.back]

        self.size -= 1

        if self.size == 0:
            self.front = None
            self.back = None
            return value

        if front:
            self.front = (self.front + 1) % self.capacity
        else:
            self.back = (self.back - 1) % self.capacity

        if self.size <= self.capacity // 4 and self.capacity // 2 >= 4:
            self.shrink()

        return value

    def grow(self) -> None:
        """Double the capacity and unroll the deque into a new list."""
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity

        if not self.is_empty():
            for i in range(self.size):
                old_index = (self.front + i) % self.capacity
                new_queue[i] = self.queue[old_index]

            self.front = 0
            self.back = self.size - 1

        self.queue = new_queue
        self.capacity = new_capacity

    def shrink(self) -> None:
        """Halve the capacity and unroll the deque into a new list."""
        new_capacity = max(4, self.capacity // 2)
        new_queue = [None] * new_capacity

        if not self.is_empty():
            for i in range(self.size):
                old_index = (self.front + i) % self.capacity
                new_queue[i] = self.queue[old_index]

            self.front = 0
            self.back = self.size - 1

        self.queue = new_queue
        self.capacity = new_capacity


def find_max_wind_speeds(numbers: List[int], size: int) -> List[int]:
    """Return the maximum value in each sliding window."""
    if not numbers:
        return []

    deque = CircularDeque()
    result = []

    for i in range(len(numbers)):

        # Remove indices that are outside the current window.
        while not deque.is_empty() and deque.front_element() <= i - size:
            deque.dequeue(front=True)

        # Remove values smaller than or equal to the current value.
        while not deque.is_empty() and numbers[deque.back_element()] <= numbers[i]:
            deque.dequeue(front=False)

        # Add the current index to the back.
        deque.enqueue(i, front=False)

        # Record the maximum once the first complete window exists.
        if i >= size - 1:
            result.append(numbers[deque.front_element()])

    return result


def execute_command_buffer(commands: List[Tuple[str, ...]], max_size: int) -> List[str]:
    """Execute commands in a capped double-ended buffer."""
    buffer = CircularDeque()

    for command in commands:

        if command[0] == "push_front":
            buffer.enqueue(command[1], front=True)

            if len(buffer) > max_size:
                buffer.dequeue(front=False)

        elif command[0] == "push_back":
            buffer.enqueue(command[1], front=False)

            if len(buffer) > max_size:
                buffer.dequeue(front=True)

        elif command[0] == "pop_front":
            buffer.dequeue(front=True)

        elif command[0] == "pop_back":
            buffer.dequeue(front=False)

    result = []

    for i in range(buffer.size):
        index = (buffer.front + i) % buffer.capacity
        result.append(buffer.queue[index])

    return result
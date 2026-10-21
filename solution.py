"""
Avaloka (Guruvai Sciences) - AI / Multi-Agent Systems Intern
Take-home Assignment: Data Structures & Systems Design
Author: Ganesh Barmavath

Problem 1: LRU Cache (hash map + doubly linked list, O(1) get / put)
Problem 2: Event Scheduler (sorting + min-heap)
"""

import heapq


# ---------------------------------------------------------------------------
# Problem 1: LRU Cache
# ---------------------------------------------------------------------------

class _Node:
    """One entry in the doubly linked list."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}                 # key -> _Node
        # Sentinel (dummy) head and tail so insertions/removals never
        # need special cases for empty ends.
        # head.next  = most recently used,  tail.prev = least recently used
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # -- internal helpers (all O(1) pointer work) ---------------------------
    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_to_front(node)

    # -- public API ---------------------------------------------------------
    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if node is None:
            return -1
        self._move_to_front(node)       # a read also counts as "used"
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if node is not None:            # update existing key
            node.value = value
            self._move_to_front(node)
            return

        node = _Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        if len(self.cache) > self.capacity:   # evict least recently used
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ---------------------------------------------------------------------------
# Problem 2: Event Scheduler
# ---------------------------------------------------------------------------

def can_attend_all(events) -> bool:
    """True if no two events overlap. Adjacent events (end == start) are OK."""
    if len(events) <= 1:
        return True
    ordered = sorted(events, key=lambda e: e[0])
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:   # starts before previous ends
            return False
    return True


def min_rooms_required(events) -> int:
    """Minimum rooms so every event can run; reuses a room as soon as it frees."""
    if not events:
        return 0
    ordered = sorted(events, key=lambda e: e[0])
    end_times = []                       # min-heap of end times of rooms in use
    heapq.heappush(end_times, ordered[0][1])
    rooms = 1
    for start, end in ordered[1:]:
        if end_times[0] <= start:       # earliest-ending room is free again
            heapq.heapreplace(end_times, end)
        else:                            # all rooms busy -> need a new one
            heapq.heappush(end_times, end)
            rooms = max(rooms, len(end_times))
    return rooms


def assign_rooms(events):
    """Extension discussed in the analysis: give each event a room number.

    Returns a list of (event, room_number) in the ORIGINAL input order.
    Room numbers start at 1. A freed room number is reused before a new
    room is opened.
    """
    indexed = sorted(enumerate(events), key=lambda p: p[1][0])
    busy = []        # min-heap of (end_time, room_number)
    free = []        # min-heap of room numbers that have become available
    next_room = 0
    result = [None] * len(events)

    for idx, (start, end) in indexed:
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if free:
            room = heapq.heappop(free)
        else:
            next_room += 1
            room = next_room
        heapq.heappush(busy, (end, room))
        result[idx] = ((start, end), room)
    return result


# ---------------------------------------------------------------------------
# Quick self-checks (run: python solution.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # LRU Cache - classic sequence, capacity 2
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                          # evicts key 2
    assert c.get(2) == -1
    c.put(4, 4)                          # evicts key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    c.put(4, 44)                         # update in place, no eviction
    assert c.get(4) == 44
    assert LRUCache(1).get(99) == -1

    # Event Scheduler
    assert can_attend_all([(9, 10), (10, 11), (11, 12)]) is True   # adjacent OK
    assert can_attend_all([(9, 11), (10, 12)]) is False
    assert can_attend_all([]) is True
    assert can_attend_all([(5, 6)]) is True

    assert min_rooms_required([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms_required([(9, 10), (9, 11), (10, 12)]) == 2
    assert min_rooms_required([(1, 5), (2, 6), (3, 7)]) == 3
    assert min_rooms_required([]) == 0

    assigned = assign_rooms([(9, 10), (9, 11), (10, 12)])
    assert assigned == [((9, 10), 1), ((9, 11), 2), ((10, 12), 1)], assigned

    print("All checks passed.")
    print("assign_rooms demo:", assigned)

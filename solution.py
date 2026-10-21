"""
Avaloka (Guruvai Sciences) — AI / Multi-Agent Systems Intern assignment
Ganesh Barmavath
Problem 1: LRU Cache | Problem 2: Event Scheduler
"""

import heapq
import threading


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # dummy head and tail; head side = most recent, tail side = oldest
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node):
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return
        node = _Node(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


def can_attend_all(events) -> bool:
    if len(events) <= 1:
        return True
    ordered = sorted(events, key=lambda e: e[0])
    for i in range(1, len(ordered)):
        if ordered[i][0] < ordered[i - 1][1]:
            return False
    return True


def min_rooms_required(events) -> int:
    if not events:
        return 0
    ordered = sorted(events, key=lambda e: e[0])
    end_times = []
    heapq.heappush(end_times, ordered[0][1])
    rooms = 1
    for start, end in ordered[1:]:
        if end_times[0] <= start:
            heapq.heapreplace(end_times, end)
        else:
            heapq.heappush(end_times, end)
            rooms = max(rooms, len(end_times))
    return rooms


def assign_rooms(events):
    indexed = sorted(enumerate(events), key=lambda p: p[1][0])
    busy = []
    free = []
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


class ThreadSafeLRUCache(LRUCache):
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._lock = threading.Lock()

    def get(self, key: int) -> int:
        with self._lock:
            return super().get(key)

    def put(self, key: int, value: int) -> None:
        with self._lock:
            return super().put(key, value)


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    c.put(4, 44)
    assert c.get(4) == 44
    assert LRUCache(1).get(99) == -1

    assert can_attend_all([(9, 10), (10, 11), (11, 12)]) is True
    assert can_attend_all([(9, 11), (10, 12)]) is False
    assert can_attend_all([]) is True

    assert min_rooms_required([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms_required([(9, 10), (9, 11), (10, 12)]) == 2
    assert min_rooms_required([(1, 5), (2, 6), (3, 7)]) == 3
    assert min_rooms_required([]) == 0

    assigned = assign_rooms([(9, 10), (9, 11), (10, 12)])
    assert assigned == [((9, 10), 1), ((9, 11), 2), ((10, 12), 1)], assigned

    tc = ThreadSafeLRUCache(2)
    tc.put(1, 1); tc.put(2, 2); tc.put(3, 3)
    assert tc.get(1) == -1 and tc.get(3) == 3

    def hammer(cache, n):
        for i in range(n):
            cache.put(i % 50, i)
            cache.get(i % 50)

    threads = [threading.Thread(target=hammer, args=(tc, 500)) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(tc.cache) <= tc.capacity

    print("All checks passed.")
    print("assign_rooms demo:", assigned)

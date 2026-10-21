"""
Tests for solution.py — Ganesh Barmavath
Run: python3 test_solution.py
"""

import random
import threading

from solution import LRUCache, ThreadSafeLRUCache, can_attend_all, \
    min_rooms_required, assign_rooms


def brute_max_overlap(events):
    # slow and simple: +1 at every start, -1 at every end,
    # ends counted before starts at the same time
    points = []
    for start, end in events:
        points.append((start, 1))
        points.append((end, -1))
    points.sort(key=lambda p: (p[0], p[1]))
    running = best = 0
    for _, change in points:
        running += change
        best = max(best, running)
    return best


def test_lru():
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
    assert c.get(3) == 3
    assert LRUCache(1).get(99) == -1

    tc = ThreadSafeLRUCache(2)
    tc.put(1, 1); tc.put(2, 2); tc.put(3, 3)
    assert tc.get(1) == -1 and tc.get(3) == 3
    print("LRU cache tests passed.")


def test_scheduler_random(trials=500):
    random.seed(42)
    for _ in range(trials):
        events = []
        for _ in range(random.randint(0, 9)):
            start = random.randint(0, 20)
            events.append((start, start + random.randint(1, 6)))

        expected_rooms = brute_max_overlap(events)
        assert min_rooms_required(events) == expected_rooms, events
        assert can_attend_all(events) == (expected_rooms <= 1), events

        assigned = assign_rooms(events)
        rooms_used = max((room for _, room in assigned), default=0)
        assert rooms_used == expected_rooms, (events, assigned)
        assert [event for event, _ in assigned] == events, (events, assigned)

        # in one room, no two events should overlap
        by_room = {}
        for (s, e), room in assigned:
            by_room.setdefault(room, []).append((s, e))
        for room, evs in by_room.items():
            evs.sort()
            for i in range(1, len(evs)):
                assert evs[i][0] >= evs[i - 1][1], (events, assigned)
    print(f"Scheduler tests passed on {trials} random event sets.")


def test_thread_safe_stress(threads_count=8, ops_per_thread=2000):
    cache = ThreadSafeLRUCache(16)

    def worker(seed):
        rng = random.Random(seed)
        for _ in range(ops_per_thread):
            key = rng.randint(0, 49)
            if rng.random() < 0.5:
                cache.put(key, rng.randint(0, 1000))
            else:
                cache.get(key)

    threads = [threading.Thread(target=worker, args=(i,))
               for i in range(threads_count)]
    for t in threads: t.start()
    for t in threads: t.join()

    assert len(cache.cache) <= cache.capacity

    forward = []
    node = cache.head.next
    while node is not cache.tail:
        forward.append(node.key)
        node = node.next
    backward = []
    node = cache.tail.prev
    while node is not cache.head:
        backward.append(node.key)
        node = node.prev

    assert forward == backward[::-1]
    assert len(forward) == len(cache.cache)
    assert set(forward) == set(cache.cache.keys())
    print(f"Thread-safety stress test passed "
          f"({threads_count} threads x {ops_per_thread} random get/put).")


if __name__ == "__main__":
    test_lru()
    test_scheduler_random()
    test_thread_safe_stress()
    print("All tests passed.")

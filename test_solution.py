"""
Tests for solution.py — Avaloka (Guruvai Sciences) assignment.
Author: Ganesh Barmavath

Run:  python3 test_solution.py

What is tested:
1. LRU Cache: the standard capacity-2 sequence, update-in-place, and
   cache misses returning -1.
2. Event Scheduler: can_attend_all, min_rooms_required and assign_rooms
   are compared against a slow but simple brute-force method on 500
   randomly generated sets of events (random seed is fixed, so the
   same 500 sets are checked every run).

The brute-force method counts, for the room problem, the maximum number
of events running at the same time by collecting every start (+1) and
end (-1) point and walking through them in order. An event that ends at
the same time another starts is counted as finished first, because
adjacent events are not overlaps.
"""

import random

from solution import LRUCache, ThreadSafeLRUCache, can_attend_all, \
    min_rooms_required, assign_rooms


def brute_max_overlap(events):
    points = []
    for start, end in events:
        points.append((start, 1))    # one more event starts
        points.append((end, -1))     # one event ends
    # at the same time value, endings (-1) come before beginnings (+1)
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
    c.put(3, 3)                      # evicts key 2
    assert c.get(2) == -1
    c.put(4, 4)                      # evicts key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    c.put(4, 44)                     # update in place, no eviction
    assert c.get(4) == 44
    assert LRUCache(1).get(99) == -1

    tc = ThreadSafeLRUCache(2)       # thread-safe version, same behaviour
    tc.put(1, 1); tc.put(2, 2); tc.put(3, 3)
    assert tc.get(1) == -1 and tc.get(3) == 3
    print("LRU cache tests passed.")


def test_scheduler_random(trials=500):
    random.seed(42)                  # fixed seed: same sets every run
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
        # events must come back in the original order
        assert [event for event, _ in assigned] == events, (events, assigned)
    print(f"Scheduler tests passed on {trials} random event sets "
          f"(brute-force comparison).")


if __name__ == "__main__":
    test_lru()
    test_scheduler_random()
    print("All tests passed.")

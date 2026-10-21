# Avaloka (Guruvai Sciences) — Data Structures & Systems Design Assignment

Take-home assignment for the **AI / Multi-Agent Systems Intern** role at Avaloka (Guruvai Sciences).

**Author:** Ganesh Barmavath · **Language:** Python 3 (standard library only)

## Contents

| File | Description |
|---|---|
| `solution.py` | Both problem solutions, plus the room-assignment extension discussed in the analysis. Self-checks run when the file is executed directly. |

## Problem 1: LRU Cache

`LRUCache` with O(1) average `get` and `put`, built from the classic pairing:

- A **hash map** (`dict`) maps each key directly to its node — O(1) lookup.
- A **doubly linked list** keeps entries in usage order (front = most recently used, back = least recently used). Moving a node to the front and evicting the tail node are pure pointer updates — O(1).
- Dummy **head/tail sentinel nodes** remove all empty-list special cases.

A `get` counts as a use and refreshes the entry's position, exactly like a `put`.

## Problem 2: Event Scheduler

- `can_attend_all(events)` — sorts by start time and checks neighbouring events for overlap. Adjacent events (`end == start`) are not overlaps. O(n log n).
- `min_rooms_required(events)` — walks events in start-time order with a **min-heap of end times** of rooms in use. If the earliest-ending room frees at or before the next event starts, it is reused; otherwise a new room opens. The largest heap size is the answer — it equals the maximum number of events running simultaneously. O(n log n) time, O(n) space.
- `assign_rooms(events)` — extension from the analysis section: the same heap walk, with heap entries as `(end_time, room_number)` and a pool of freed room numbers, returning `((start, end), room_number)` pairs in the original input order.

## Running the checks

```bash
python3 solution.py
# All checks passed.
# assign_rooms demo: [((9, 10), 1), ((9, 11), 2), ((10, 12), 1)]
```

The self-checks cover the standard capacity-2 LRU sequence (including update-in-place and cache misses returning `-1`) and the scheduler examples from the brief. Both scheduler functions were additionally cross-checked against a brute-force sweep-line count of maximum simultaneous events on 500 randomly generated event sets.

## Complexity summary

| Function | Time | Space |
|---|---|---|
| `LRUCache.get` / `put` | O(1) average | O(1) extra, O(capacity) total |
| `can_attend_all` | O(n log n) | O(n) |
| `min_rooms_required` | O(n log n) | O(n) |
| `assign_rooms` | O(n log n) | O(n) |

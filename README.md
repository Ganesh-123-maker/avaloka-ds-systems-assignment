# Avaloka (Guruvai Sciences) — Data Structures & Systems Design Assignment

Take-home assignment for the **AI / Multi-Agent Systems Intern** role at Avaloka (Guruvai Sciences).

**Author:** Ganesh Barmavath · **Language:** Python 3 (standard library only)

## Files in this repo

- `solution.py` — both problem solutions, plus the room-assignment function from Question 3 of the analysis. When you run this file, it also runs its own small checks.
- `Ganesh_Barmavath_Avaloka_Assignment.pdf` — the full written submission. For each problem, I have first explained my approach in simple words, and then given the code. At the end, I have answered all four questions in the Final Discussion & Analysis section.

## Problem 1: LRU Cache

I used two data structures together, because one alone was not enough.

- **Hash map (dictionary):** it gives me the item for a key directly, without searching through all the items. So this part is fast, O(1).
- **Doubly linked list:** I keep all the items in the order they were used. The front of the list is the item used most recently, and the last item is the oldest one. When an item is used, I remove it from its place and put it at the front. This only means changing a few links, so this is also O(1).
- The dictionary also points to the item's place (node) in the list. That is the important part — because of this, I never search in the list.
- I also used two dummy nodes, one at the start and one at the end of the list. They do not store any data. They only make the code simple, so I don't need separate checks for an empty list.
- One more point: even a `get` call counts as a use, so `get` also moves the item to the front, not only `put`.

## Problem 2: Event Scheduler

- **`can_attend_all(events)`:** I first sort the events by start time. After sorting, I only check each event with the one just before it. If an event starts before the previous event has ended, there is an overlap and the answer is False. If one event ends at 10 and the next starts at 10, that is not an overlap.
- **`min_rooms_required(events)`:** the number of rooms needed is equal to the maximum number of events going on at the same time. I go through the events in start-time order and keep the end times of the busy rooms in a min-heap, so the room that will become free first is always at the top. If that room has ended before the new event starts, I give the same room to this event. If not, I take one more room.
- **`assign_rooms(events)`:** this is the extension from Question 3. It does the same work as above, but it also remembers which room each event got, and returns the answer in the same order in which the events were given.

## Complexity, in points

- **`LRUCache.get` — Time: O(1), Extra space: O(1).** I search the key in the dictionary and change a few links to bring the node to the front. These are small, fixed steps.
- **`LRUCache.put` — Time: O(1), Extra space: O(1).** It is also the same. If the cache is full, I remove the last node, which also takes only a few steps.
- **LRU Cache total memory — Space: O(capacity).** For every item, I store one node in the list and one entry in the dictionary.
- **`can_attend_all` — Time: O(n log n), Extra space: O(n).** Most of the time goes in sorting. After sorting, I go through the list only one time.
- **`min_rooms_required` — Time: O(n log n), Extra space: O(n).** Sorting takes O(n log n) time, and for every event I do one heap work, which takes O(log n) time.
- **`assign_rooms` — Time: O(n log n), Extra space: O(n).** It does the same steps as `min_rooms_required`, with one more small heap for the room numbers that have become free.

Here O(1) means average time. A dictionary is very fast in normal cases, but in a rare case where many keys get the same hash, it can become slow.

## How to run the checks

```
python3 solution.py
```

Output:

```
All checks passed.
assign_rooms demo: [((9, 10), 1), ((9, 11), 2), ((10, 12), 1)]
```

For testing, I ran the standard capacity-2 example for the LRU cache and checked each answer one by one. For the scheduler, I also compared my answers with a small brute-force program on 500 random sets of events, including empty lists and lists with only one event. All the answers matched.

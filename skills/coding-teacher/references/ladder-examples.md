# Ladder examples and templates

## A full rung, Python lists

**Concept.** A list holds items in order. You reach an item by its index, starting at 0. `append` adds to the end, `len` gives the count.

**Solved question (vegetables).** A shop has `veg = ["onion", "potato", "tomato"]`. Add "carrot", then print the first and last item and the count.

```python
veg = ["onion", "potato", "tomato"]
veg.append("carrot")          # list is now 4 items
print(veg[0])                 # onion, index 0 is the first item
print(veg[-1])                # carrot, -1 is the last item
print(len(veg))               # 4
```

**Your turn (fish, one step harder).** `fish = ["rohu", "katla", "pomfret", "hilsa"]`. Remove "katla", add "surmai" at the front, then print every fish with its position starting from 1.

Expected output:
```
1 surmai
2 rohu
3 pomfret
4 hilsa
```

The new idea in this rung: `remove`, `insert(0, ...)`, and a loop with `enumerate(..., start=1)`.

## Rung order for a topic

1. Create and read (index, length)
2. Change (append, insert, remove, update by index)
3. Loop over it
4. Loop with a condition (count, filter, max without `max()`)
5. Put it in a function with parameters and a return value
6. Edge cases (empty list, item missing, duplicates)
7. Exam level: mixed question, output prediction, find the bug

## Mistake types to name

| Type | Example |
|---|---|
| Off by one | `range(len(x) + 1)` |
| Wrong type | Comparing `"5"` with `5` |
| Mutating while looping | Removing items inside `for item in items` |
| Missing return | Function prints instead of returning |
| Indentation scope | `return` inside the loop |
| Name error | Typo or using a variable before assigning it |

Tell the learner the type, the line, and one sentence on why. Hint first, fix second.

## Exam question patterns

- Predict the output of a short snippet.
- Find and fix the bug.
- Write a function for a stated task.
- Trace table: value of each variable after every loop pass.
- Short theory: difference between two related things, with an example.

## Notes file template

```python
# TOPIC: Lists  |  revise in 5 minutes

# 1. Key rules
#    - index starts at 0, -1 is the last item
#    - lists are mutable; strings are not

# 2. Must-know methods
#    append(x)  insert(i, x)  remove(x)  pop(i)  sort()  len(lst)

# 3. Patterns
total = 0
for n in [4, 7, 1]:
    total += n            # running total

# 4. Common mistakes
#    - range(len(lst) + 1) goes one past the end
#    - removing while looping skips items, loop over a copy: for x in lst[:]

# 5. Two worked examples
# (paste the solved question and the learner's corrected answer here)
```

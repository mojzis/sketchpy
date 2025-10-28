# Help: Lists

## Quick Reference

### Creating Lists
```python
colors = ["red", "blue", "green"]
numbers = [10, 20, 30, 40]
mixed = ["text", 42, True]  # Lists can hold different types
```

### Accessing Elements
```python
colors = ["red", "blue", "green"]
#         [0]    [1]     [2]

first = colors[0]   # "red"
second = colors[1]  # "blue"
last = colors[2]    # "green"
last = colors[-1]   # "green" (negative indices count from end)
```

### List Functions
```python
len(colors)         # Returns number of items (3)
colors.append("yellow")  # Adds item to end
colors[1] = "purple"     # Changes item at index 1
```

### Using Lists in Loops
```python
# Method 1: Use indices
for i in range(len(colors)):
    color = colors[i]

# Method 2: Use enumerate
for i, color in enumerate(colors):
    # i is the index, color is the value

# Method 3: Just iterate values
for color in colors:
    # Just gives you the values, no index
```

## Common Errors

### Error: "IndexError: list index out of range"
**What it means:** Trying to access an index that doesn't exist
**How to fix:**
- List with 5 items has indices 0-4
- Use `len(my_list)` to check length
- Make sure `i` is less than `len(my_list)`

### Error: "TypeError: list indices must be integers, not float"
**What it means:** Using a decimal number as an index
**How to fix:** Convert to integer: `colors[int(2.5)]` or ensure index is whole number

### Error: Getting the same value every time
**What it means:** Not using the loop variable to access different indices
**How to fix:** Use `colors[i]` inside the loop, not `colors[0]`

### Error: "NameError: name 'enumerate' is not defined"
**What it means:** Actually, `enumerate` is built-in and should always work
**How to fix:** Check spelling: `enumerate` not `enumarate`

## Debugging Tips

1. **Print the list:** Use `print(colors)` to see all items
2. **Print indices and values:** Add `print(f"i={i}, value={colors[i]}")`
3. **Check list length:** Print `len(my_list)` to verify size
4. **Test with small lists:** Start with 2-3 items before scaling up

## List Patterns

### Parallel Lists
```python
# Store related data in multiple lists
names = ["Rose", "Tulip", "Daisy"]
colors = ["pink", "yellow", "white"]
sizes = [20, 18, 22]

for i in range(len(names)):
    # names[i], colors[i], and sizes[i] all describe the same flower
```

### List Length Flexibility
```python
# Works for any list length!
for i in range(len(my_list)):
    # Add/remove items from my_list and loop adapts
```

### Enumerate Examples
```python
flowers = ["Rose", "Tulip", "Daisy"]

for index, name in enumerate(flowers):
    print(f"{index}: {name}")
# Output:
# 0: Rose
# 1: Tulip
# 2: Daisy

# Start counting from 1 instead of 0
for index, name in enumerate(flowers, start=1):
    print(f"{index}: {name}")
# Output:
# 1: Rose
# 2: Tulip
# 3: Daisy
```

## Related Lessons
- **Lesson 6:** For loops - now we're storing different values for each iteration
- **Next:** Lesson 8 uses nested loops with more complex data

## Extra Challenges

1. **Three properties:** Create lists for colors, sizes, and names
2. **Reverse order:** Draw flowers from the list backwards using `colors[::-1]`
3. **Repeated pattern:** Use modulo with list length: `colors[i % len(colors)]`
4. **Sort the list:** Try `sorted(flowers)` to alphabetize
5. **Random selection:** Import `random` and use `random.choice(colors)`
6. **Find max/min:** Use `max(sizes)` or `min(sizes)` from a numbers list

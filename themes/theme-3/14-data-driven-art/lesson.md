## ⭕ Project 14: Data-Driven Art

### Goal
Create art from data! Define mandalas as dictionaries in a list, then draw them all with a loop.

### What you'll learn
- Dictionaries (key-value pairs)
- Lists of dictionaries
- Accessing dictionary values with `config['key']`
- Separating data from code (data-driven design)

### Dictionaries Store Related Data
Instead of separate variables, group them:

```python
mandala_config = {
    'x': 200,
    'y': 200,
    'circles': 8,
    'color': MathDoodlingPalette.MIST_BLUE
}
```

Access values: `mandala_config['x']` → 200

### List of Dictionaries
Store multiple configurations:

```python
mandalas = [
    {'x': 200, 'y': 200, 'circles': 8, ...},
    {'x': 600, 'y': 200, 'circles': 12, ...},
    {'x': 400, 'y': 450, 'circles': 6, ...}
]
```

### Steps
1. Create a list called `mandalas`
2. Each item is a dictionary with mandala properties
3. Loop through the list: `for config in mandalas:`
4. Draw each mandala using values from `config`
5. Result: Easy to add/remove/modify mandalas!

### Why This Is Professional
Real programs separate **data** (what to draw) from **logic** (how to draw). Want to add a mandala? Just add another dictionary!

### Challenge
- Add 5 more mandalas to the list
- Add a `'visible': True/False` key and only draw if True
- Load configuration from a file (advanced!)

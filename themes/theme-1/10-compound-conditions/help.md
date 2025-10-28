## Additional Help

### Common Issues

**Conditions not working as expected?**

- Check your comparison operators: `==` (equals), `>` (greater than), `<` (less than)
- Remember: `=` assigns a value, `==` compares values
- Use parentheses to group complex conditions: `(a and b) or c`

**Boolean variables confusing?**

- `is_weekend = True` or `is_weekend = False` (capital T/F)
- You can use them directly: `if is_weekend:` instead of `if is_weekend == True:`
- Use `not` to invert: `if not is_weekend:` (true on weekdays)

**Wrong branch executing?**

- Python checks conditions from top to bottom
- The first condition that's true will execute
- Make sure your `elif` and `else` are aligned with the `if`

### Understanding Logical Operators

**`and` - Both must be true:**

```python
if age >= 16 and has_license:
    # Only true when age is 16+ AND has_license is True
```

**`or` - Either can be true:**

```python
if is_weekend or is_holiday:
    # True when it's weekend OR holiday (or both!)
```

**`not` - Inverts the condition:**

```python
if not is_raining:
    # True when is_raining is False
```

### Tips

- Start with simple conditions, then combine them
- Test each variable value to see how it affects the result
- Use `can.text()` to display variable values for debugging
- Build complex logic step by step - add one condition at a time
- Comment your conditions to explain the logic

### Debugging Strategy

1. Print or display variable values with `can.text()`
2. Test each condition separately before combining
3. Use parentheses to make complex conditions clear
4. Try extreme values (0, 100) to test edge cases

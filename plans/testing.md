# Test Output Management for Token Efficiency

## Writing Silent Tests

### Test Design Principles
- Use assertion libraries that provide clear, minimal failure messages
- Avoid verbose logging in test code unless debugging specific issues
- Structure tests so failures are self-explanatory from the assertion alone
- Name tests descriptively: `test_oauth_token_refresh_after_expiry` not `test_1`

### Python/Pytest Best Practices
```python
# GOOD - Clear assertion, minimal output when passing
def test_user_authentication():
    user = authenticate(username="test", password="pass123")
    assert user.is_authenticated
    assert user.role == "admin"

# AVOID - Verbose print statements
def test_user_authentication():
    print(f"Testing authentication for user: test")
    user = authenticate(username="test", password="pass123")
    print(f"User object: {user}")
    print(f"Authentication status: {user.is_authenticated}")
    assert user.is_authenticated
```

## Running Pytest for Minimal Output

### For Passing Tests (Default Mode)
```bash
# Minimal output - only show summary
pytest -q

# Even more concise
pytest --tb=no -q

# Just counts (most token-efficient)
pytest --tb=no -q --no-header
```

### For Failing Tests (Debugging Mode)
```bash
# Short traceback with essential context
pytest --tb=short

# Show only the first/last N failures
pytest --maxfail=3 --tb=short

# Full detail only when needed
pytest -vv --tb=long  # Use sparingly
```

## Token-Optimized Output Strategy

### Output Levels by Situation

**Default (Passing Tests):**
```
✓ 142 passed in 15.3s
Cost: $0.43 (12,450 tokens)
```

**On Failure (Summary First):**
```
✗ 3/145 failed in auth module
- test_oauth_token_refresh: AssertionError at line 78
- test_session_expiry: Expected 401, got 200
- test_password_hash: bcrypt comparison failed

[Full details available - run with --tb=short for traces]
```

**Deep Debugging (On Request Only):**
```bash
# Only when actively debugging
pytest tests/auth/test_oauth.py::test_token_refresh -vv --tb=long
```

## Integration with AI Agents

### Environment Variables
```bash
# For agent-driven testing
export PYTEST_OPTS="--tb=short -q --no-header"

# Run tests
pytest $PYTEST_OPTS tests/
```

### Pytest Configuration (pytest.ini or pyproject.toml)
```ini
[tool.pytest.ini_options]
# Default: silent passing tests
addopts = "-q --tb=short --no-header"

# Override when debugging
# pytest -vv --tb=long
```

### Capture Output Selectively
```python
# In tests, use capsys to control output
def test_api_call(capsys):
    result = api.call()
    # Output only captured on failure
    if not result.success:
        print(f"API Error: {result.error}")
    assert result.success
```

## Cost Optimization Rules

1. **Always omit passing test output** (saves 10-100x tokens)
2. **Use --tb=short for failures** (2-5x reduction vs full traces)
3. **Filter to failing tests only**: `pytest --lf` (last failed)
4. **Limit failure details**: `--maxfail=5` stops after 5 failures
5. **Store full logs externally**: Redirect verbose output to files

### Example Agent Tool Configuration
```python
def run_tests(verbose: bool = False) -> str:
    """Run test suite with appropriate verbosity for context."""
    if verbose:
        # Only for debugging - costs 10x more tokens
        result = subprocess.run(["pytest", "-v", "--tb=short"])
    else:
        # Default: minimal output
        result = subprocess.run(["pytest", "-q", "--tb=no"])
    
    return {
        "summary": f"{passed} passed, {failed} failed",
        "failures": extract_failure_summaries(),  # Structured list
        "full_log_path": "/tmp/pytest_output.txt"  # Reference only
    }
```

## Progressive Disclosure Pattern

When agent encounters test failures:

1. **First Pass**: Show only summary (counts + failure names)
2. **Second Pass**: If agent requests details, show --tb=short
3. **Third Pass**: If still debugging, provide --tb=long for specific test

This reduces initial token usage by 20-50x while maintaining debugging capability.

## Key Pytest Flags Reference

| Flag | Purpose | Token Impact |
|------|---------|--------------|
| `-q` | Quiet mode | -5x |
| `--tb=no` | No traceback | -10x |
| `--tb=short` | Minimal traceback | -3x |
| `--tb=line` | One line per failure | -5x |
| `--no-header` | No header/footer | -2x |
| `-x` | Stop on first failure | Variable |
| `--lf` | Run last failed only | -10x+ |
| `--maxfail=N` | Stop after N failures | Variable |

## Implementation Checklist

- [ ] Configure pytest.ini with `-q --tb=short --no-header`
- [ ] Remove print/logging from passing test paths
- [ ] Structure test names to be self-documenting
- [ ] Create agent tool that returns structured failure data
- [ ] Store full logs to filesystem, pass only references to agent
- [ ] Use `--lf` flag when iterating on failures
- [ ] Monitor token usage per test run in observability platform
# Env parser

Use `pip install parsenv`

## Example

```py
import env

assert env.get("TOKEN") == "abc123"
assert env.get("X", False) is False
assert env.get_int("PORT") == 123
assert env.get_strs("KEYS", []) == ["word1", "F402", "12"]
assert env.get_ints("ADMIN_IDS") == [1, 2, 3]
assert env.get_ints("X", 0) == 0

try:
    env.get("X")
except KeyError as e:
    assert str(e) == "Environment variable `X` not set"

try:
    env.get_ints("BAD_NUMS")
except ValueError as e:
    assert (
            str(e) == "Can't parse environment variable `BAD_NUMS`: "
                      "invalid literal for int() with base 10: 'a'"
    )
```

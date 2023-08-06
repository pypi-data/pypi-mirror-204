def parse_strs(text: str) -> list[str]:
    return [i.strip() for i in text.strip().split(",")]


def parse_ints(text: str) -> list[int]:
    return [int(i) for i in parse_strs(text)]


def parse_bool(text: str) -> bool:
    text = text.lower()
    if text in ["y", "yes", "t", "true", "on", "1"]:
        return True
    if text in ["n", "no", "f", "false", "off", "0"]:
        return False
    _ = f"Can't parse bool from `{text}`"
    raise ValueError(_)

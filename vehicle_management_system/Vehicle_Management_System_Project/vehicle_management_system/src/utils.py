def read_int(prompt, minimum=None, maximum=None):
    value = int(input(prompt).strip())
    if minimum is not None and value < minimum:
        raise ValueError(f"Value must be at least {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"Value must be at most {maximum}.")
    return value


def read_float(prompt, minimum=None):
    value = float(input(prompt).strip())
    if minimum is not None and value < minimum:
        raise ValueError(f"Value must be at least {minimum}.")
    return value


def pause():
    input("\nPress Enter to continue...")


def print_table(rows, headers):
    if not rows:
        print("No records found.")
        return
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    line = "-+-".join("-" * width for width in widths)
    print(line)
    print(" | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers)))
    print(line)
    for row in rows:
        print(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))
    print(line)

import json
import re
import sys


def scrub_item(item):
    if isinstance(item, list):
        new_item = [scrub_item(sub_item) for sub_item in item]
    elif isinstance(item, bool):
        new_item = "-"
    elif isinstance(item, int) or isinstance(item, float):
        new_item = scrub_item(str(item))
    elif isinstance(item, dict):
        new_item = {k: scrub_item(v) for k, v in item.items()}
    else:
        new_item = re.sub(r"\w", "*", item)
    return new_item


def scrub(sensitive, input):
    """take list of fields and dict and return new dict with scrubbed fields"""
    scrubbed = {}
    for k, v in input.items():
        if k in sensitive:
            scrubbed[k] = scrub_item(v)
        elif isinstance(v, dict):
            scrubbed[k] = scrub(sensitive, v)
        else:
            scrubbed[k] = v
    return scrubbed


def main():
    sens_file = sys.argv[1]
    in_file = sys.argv[2]
    with open(sens_file, "r") as f:
        sensitive = [line.strip() for line in f.readlines()]
    with open(in_file, "r") as f:
        input = json.load(f)
    print(scrub(sensitive, input))


if __name__ == "__main__":
    main()

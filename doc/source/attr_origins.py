import re
import sys

p_strip_memaddress = re.compile(r"^(.*) at 0x[0-9A-F]+>$", re.I)

def strip_memaddress(desc_str):
    m = p_strip_memaddress.match(desc_str)

    if m:
        return m.group(1) + ">"
    else:
        return desc_str

def attr_origins(cls):
    skipped_attrs = ["__dict__", "__doc__"]
    attrs = [m for m in dir(cls) if m not in skipped_attrs]

    width = 1 + max(len(a) for a in attrs)

    descs = {a: strip_memaddress(repr(getattr(cls, a))) for a in attrs}

    print(*(f"{a: <{width}} :: {descs[a]}" for a in attrs), sep="\n")


if __name__ == "__main__":
    exec(f"from {sys.argv[1]} import {sys.argv[2]}", globals())

    attr_origins(eval(sys.argv[2]))

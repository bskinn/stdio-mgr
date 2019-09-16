import re
import sys

SKIPPED_ATTRS = ["__dict__", "__doc__"]

p_strip_memaddress = re.compile(r"^(.*) at 0x[0-9A-F]+>$", re.I)


def generate_desc(cls, attr):
    """Generate the object description."""
    obj = getattr(cls, attr)

    desc = strip_memaddress(repr(obj))

    if isinstance(obj, property):
        desc = add_property_defclass(desc, cls, attr, obj)

    return desc


def add_property_defclass(desc, cls, attr, obj):
    """Inject the definition location for a property object."""
    def_cls = [
        super(c, c) for c in cls.mro() if getattr(c, attr, None) is getattr(cls, attr)
    ][-1].__thisclass__

    return desc[:-1] + f" of '{def_cls.__name__}' object>"


def strip_memaddress(desc_str):
    """Strip the reported memory address of the object, if present."""
    m = p_strip_memaddress.match(desc_str)

    if m:
        return m.group(1) + ">"
    else:
        return desc_str


def attr_origins(cls):
    """Generate the attribute inheritance information for cls."""
    attrs = [m for m in dir(cls) if m not in SKIPPED_ATTRS]

    width = 1 + max(len(a) for a in attrs)

    descs = {a: generate_desc(cls, a) for a in attrs}

    print(*(f"{a: <{width}} :: {descs[a]}" for a in attrs), sep="\n")


if __name__ == "__main__":
    exec(f"from {sys.argv[1]} import {sys.argv[2]}", globals())

    attr_origins(eval(sys.argv[2]))

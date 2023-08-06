import logging
from .source.build import Builder
import os

logging.getLogger().setLevel(logging.CRITICAL)

paths = [
    "./data/Cuckoo/",
]

work = set()
for p in paths:
    work.update(p + f for f in os.listdir(p))


for sample in work:
    b = Builder(sample)
    n = 0
    try:
        for c in b.calls():
            if c["api"] == "send":
                n += 1
        if n:
            print(sample, ":", n, "calls to send")
    except KeyError:
        pass
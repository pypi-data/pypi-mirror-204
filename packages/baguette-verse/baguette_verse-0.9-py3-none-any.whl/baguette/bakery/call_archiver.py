import json
import logging
import os
from threading import RLock, Thread, Event
from time import sleep
from code import interact
from .source.build import *
from .source.database import *
from .source.utils import extract
import argparse

parser = argparse.ArgumentParser(description="Parses all Cuckoo reports in given paths, classify their API calls, and stores them in Python databases.")

parser.add_argument("-r", "--recursive", action="store_true", help="If true, will explore given folders recursively to find Cuckoo reports.")

args1, remaining_args = parser.parse_known_args()

work : set[str] = set()
lock = RLock()

def extend_work(s : str):
    from pathlib import Path
    import glob
    with lock:
        for s in glob.iglob(s):
            p = Path(s).absolute()
            if p.is_dir():
                for pi in p.iterdir():
                    if pi.is_dir() and args1.recursive:
                        extend_work(pi)
                    elif pi.is_file() and pi.suffix == ".json":
                        work.add(pi)
            elif p.is_file() and args1.recursive:
                work.add(p)

parser.add_argument("sources", type = extend_work, action="extend", nargs = "+", help="The source files/folders to parse for API calls.")
parser.add_argument("--all_categories", action="store_true", help="If enabled, won't start an interactive prompt, but instead will compile one database for all available category (not name) of API call")

args = parser.parse_args(remaining_args)

DATA_PATH = "database.pyt"

database = Database(dict, List[List[List[List[dict]]]])
# database = Database(dict, List[dict])
running = Event()
finished = Event()


def start():
    with lock:
        running.set()
        finished.clear()

def stop():
    running.clear()

def save(path = None):
    from pickle import dump
    if path == None:
        path = DATA_PATH
    with lock:
        with open(path, "wb") as f:
            dump(database, f)
        print("Succesfully saved database.")

def size():
    with lock:
        print("Got {} types of calls and {} calls in total.".format(len(database), sum(len(li) for li in database.values())))

def remaining():
    return len(work)

def secured(func, *args, **kwargs):
    with lock:
        return func(*args, **kwargs)

fil = lambda x : True

def explorer():
    global fil
    while True:
        running.wait()
        with lock:
            if work:
                file = work.pop()
            else:
                finished.set()
                sleep(0.01)
                continue
        try:
            with open(file, "rb") as f:
                data = json.load(f)
        except:
            # print("Exception while loading file '{}':".format(file))
            # print_exc()
            continue
        E : List[List[List[dict]]] = []
        database.database.append(E)
        try:
            for p in data["behavior"]["processes"]:
                P : List[List[dict]] = []
                table : Dict[int, list] = {}
                for c in p["calls"]:
                    with lock:
                        running.wait()
                        try:
                            if fil(c):
                                if c["tid"] not in table:
                                    table[c["tid"]] = []
                                    P.append(table[c["tid"]])
                                table[c["tid"]].append(c)
                        except:
                            print(c, len(database))
                            raise
                E.append(P)
        except:
            print("Exception while analyzing file {}:".format(file))
        # for p in bf.data["behavior"]["processes"]:
        #     for c in p["calls"]:
        #         with lock:
        #             running.wait()
        #             try:
        #                 database.database.append(c)
        #             except:
        #                 print(c, len(database))
        #                 raise

def set_filter(f : Callable[[dict], bool]):
    global fil
    fil = f

def at_end(f, *args, **kwargs):
    def _wait():
        while remaining():
            sleep(0.001)
        f(*args, **kwargs)
    Thread(target = _wait, daemon = True).start()

categories = (
    "registry",
    "__notification__",
    "certificate",
    "crypto",
    "exception",
    "file",
    "iexplore",
    "misc",
    "netapi",
    "network",
    "ole",
    "process",
    "resource",
    "services",
    "synchronisation",
    "system",
    "ui"
)


t = Thread(target = explorer, daemon = True)
t.start()


if not args.all_categories:

    from Viper.interactive import InteractiveInterpreter

    env = {
        "start" : start,
        "stop" : stop,
        "save" : save,
        "size" : size,
        "remaining" : remaining,
        "search" : extend_work,
        "secured" : secured,
        "database" : database,
        "extract" : extract,
        "set_filter" : set_filter,
        "at_end" : at_end, 
        "logging" : logging,
        "categories" : categories,
        "finished" : finished
    }

    InteractiveInterpreter(env).interact("Interactive API call archiver. Use dir() to see all the available functions.")

else:

    initial_work = work.copy()

    print("About to compute databases for {} categories, using {} Cuckoo reports.".format(len(categories), len(initial_work)))

    for cat in categories:
        if not os.path.exists(cat + ".pyt"):
            database.clear()
            work.clear()
            work |= initial_work
            set_filter(lambda c : c["category"] == cat)
            print("Compiling database for category '{}'.".format(cat))
            start()
            while not finished.wait(20):
                print("Progress : {:.2f}%".format((len(initial_work) - remaining()) / remaining() * 100))
            stop()

            print("Creating 'names' view.")
            database.create_view("names", extract("api"))

            print("Saving database '{}'.".format(cat + ".pyt"))
            save(cat + ".pyt")
        else:
            print(cat + ".pyt database already exists.")
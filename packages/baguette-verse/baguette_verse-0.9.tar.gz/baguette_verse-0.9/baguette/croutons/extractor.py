"""
This module contains the extract function which is used to toast baguettes.
"""

from ..rack import BaguetteRack

__all__ = ["extract"]





def extract(rack : BaguetteRack) -> BaguetteRack:

    """
    Extracts patterns in a baguette using the data written in the given BaguetteRack object.
    Returns a BaguetteRack (the same) containing the results (and exceptions on failure).
    """

    from ..rack import BaguetteRack, TimeoutExit

    try:

        if rack.toasted:
            return rack
        
        import logging
        levels = {
            0 : logging.ERROR,
            1 : logging.WARNING,
            2 : logging.INFO,
            3 : logging.DEBUG
        }
        
        from ..bakery.logger import set_level, logger
        set_level(levels[rack.verbosity])

        logger.debug("Just change worker's verbosity level.")

        import os
        from pickle import dump, load
        from Viper.better_threading import Future, DaemonThread
        from ..bakery.source.graph import Graph

        if rack.perf:
            from ..bakery.source.utils import chrono
            chrono.enabled = True
            chrono.auto_report = True

        if not os.path.exists(rack.baguette):
            raise FileNotFoundError("Could not find baguette file: {}".format(rack.report))
        if not os.path.isfile(rack.baguette):
            raise FileExistsError("Given path to baguette file is not a file.")
        if os.path.exists(rack.extracted) and not os.path.isfile(rack.extracted):
            raise FileExistsError("Given baguette extraction file exists and is not a file.")

        result : Future[bool] = Future()

        def extract_main():
            
            try:
                logger.info("Loading baguette...")
                with rack.baguette.open("rb") as file:
                    b = load(file)

                logger.info("Loading necessary MetaGraphs...")
                patterns, pattern_names = rack.patterns, rack.pattern_names

                logger.info("Searching patterns in baguette graph...")
                matches : dict[str, list[Graph]] = {}

                for name, MG in zip(pattern_names, patterns):
                    l = list(MG.search_iter(b))
                    if l:
                        matches[name] = l

                logger.info("Exporting {} matches to file '{}'...".format(sum(len(l) for l in matches.values()), rack.extracted))
                rack.extracted.parent.mkdir(parents = True, exist_ok = True)
                with open(rack.extracted, "wb") as file:
                    dump(matches, file)

                result.set(True)
                logger.info("Done !")
            except BaseException as e:
                result.set_exception(e)

        def death_timer():
            from time import sleep
            from Viper.format import duration
            if rack.maxtime < float("inf"):
                logger.info("Death timer thread started. {} remaining.".format(duration(rack.maxtime)))
                sleep(rack.maxtime)
                logger.error("Death timer reached, about to exit.")
                result.set_exception(TimeoutExit("Toasting maxtime reached"))
            else:
                while True:
                    sleep(600)
        
        t1 = DaemonThread(target = extract_main)
        t2 = DaemonThread(target = death_timer)
        t1.start()
        t2.start()
        
        while not result.wait(0.1):
            pass
        result.result()
    
    except BaseException as e:
        from traceback import print_exc, TracebackException
        rack.exception = TracebackException.from_exception(e)
        if not isinstance(e, (KeyboardInterrupt, TimeoutExit)):
            print_exc()
    finally:
        if rack.exception is None or not issubclass(rack.exception.exc_type, (KeyboardInterrupt, TimeoutExit)):
            rack.toasted = True
        return rack





del BaguetteRack
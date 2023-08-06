from contextlib import contextmanager
from multiprocessing import Process
from time import sleep
from typing import Callable, Any, Tuple, Optional


@contextmanager
def sub_process(
    target: Callable,
    args: Optional[Tuple[Any, ...]] = None,
    name: Optional[str] = None,
    terminate: bool = True,
):
    proc = Process(target=target, args=args or (), name=name)
    proc.start()
    try:
        sleep(0.2)
        yield proc
    finally:
        if terminate:
            proc.terminate()
        proc.join()

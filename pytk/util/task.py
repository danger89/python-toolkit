import logging
import threading
import time
import traceback
import warnings

from rich.progress import Progress


logger = logging.getLogger(__file__)


class Task:
    idle = 0
    running = 1
    finished = 2
    error = 3

    def __init__(self, callable):
        self.status = Task.idle
        self.callable = callable
        self.thread = None
        self.retry = 5
        self.last_exc = None
    
    def _run(self):
        self.status = Task.running
        try:
            self.callable()
            self.status = Task.finished
        except Exception as e:
            self.status = Task.error
            self.retry -= 1
            self.last_exc = e
            traceback.print_exc()
    
    def start(self):
        if self.thread and self.thread.is_alive():
            warnings.warn("Trying to restart a task while the previous is "
                          "still running.")
        self.thread = threading.Thread(target=self._run)
        self.thread.start()


class TaskPool:
    
    def __init__(self, callables, name="", threads=35, interval=0.1):
        self.tasks = list(map(Task, callables))
        self.name = name
        self.threads = threads
        self.interval = interval
    
    def start(self):
        with Progress() as progress:
            p = progress.add_task(self.name, total=len(self.tasks))
            while self.tasks:
                running_threads = 0
                swap_tasks = []
                for task in self.tasks:
                    if task.status == Task.running:
                        running_threads += 1
                    elif task.status == Task.finished:
                        progress.update(p, advance=1)
                        continue
                    swap_tasks.append(task)
                self.tasks = swap_tasks
                for task in self.tasks:
                    if running_threads >= self.threads:
                        break
                    if task.status == Task.error and task.retry <= 0:
                        logger.fatal("Task's retries exceed limit, raising "
                                     "the latest caught error")
                        raise task.last_exc
                    if task.status in [Task.idle, Task.error]:
                        task.start()
                        running_threads += 1
                time.sleep(self.interval)

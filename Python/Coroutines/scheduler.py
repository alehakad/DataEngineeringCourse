from typing import Callable, Generator, Any
from datetime import datetime, timedelta
from priority_queue import PriorityQueue
import time


class Scheduler:

    class Sleep:
        """delay for task"""

        def __init__(self, seconds_to_sleep: int):
            self.seconds_to_sleep = seconds_to_sleep

        def __await__(self) -> Generator[None, None, None]:
            start = time.time()
            while time.time() - start < self.seconds_to_sleep:
                yield
            return

    class SchedulerTask:
        def __init__(self, func, timepoint, *args, **kwargs):
            self.func = func
            self.timepoint = timepoint
            self.args = args
            self.kwargs = kwargs

        def __lt__(self, other: "Scheduler.SchedulerTask") -> bool:
            return self.timepoint < other.timepoint

        def __call__(self):
            try:
                return next(self.func(*self.args, **self.kwargs))
            except StopIteration:
                return False

    def __init__(self):
        self.task_queue = PriorityQueue()
        self.immediate_tasks_queue = []

    def add(self, task: Callable[..., Any], timepoint: datetime, *args, **kwargs):
        self.task_queue.push(Scheduler.SchedulerTask(task, timepoint, *args, **kwargs))

    def run(self):
        while not (self.task_queue.is_empty() and len(self.immediate_tasks_queue) == 0):
            # pop next task
            if len(self.immediate_tasks_queue) != 0:
                next_task: Scheduler.SchedulerTask = self.immediate_tasks_queue.pop(0)
            else:
                next_task: Scheduler.SchedulerTask = self.task_queue.pop()
            # wait until timestamp for next task
            time.sleep(max(0, (next_task.timepoint - datetime.now()).total_seconds()))
            result = next_task()
            if result != False:
                if not (isinstance(result, int)) or result == 0:
                    self.immediate_tasks_queue.append(next_task)
                # if False is returned - task is not repeated
                elif result != False:
                    next_task.timepoint += timedelta(seconds=result)
                    self.task_queue.push(next_task)

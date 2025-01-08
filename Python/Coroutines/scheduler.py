from typing import Callable, Generator
from datetime import datetime, timedelta
from priority_queue import PriorityQueue
import time


class Scheduler:

    class SchedulerTask:
        def __init__(self, func, timepoint, frequency, *args, **kwargs):
            self.func = func
            self.timepoint = timepoint
            self.frequency = frequency
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

    def add(
        self,
        task: Callable[..., Generator],
        timepoint: datetime,
        frequency: int,
        *args,
        **kwargs
    ):
        self.task_queue.push(
            Scheduler.SchedulerTask(task, timepoint, frequency, *args, **kwargs)
        )

    def run(self):
        while not self.task_queue.is_empty():
            next_task: Scheduler.SchedulerTask = self.task_queue.pop()
            # wait until timestamp for next task
            time.sleep(max(0, (next_task.timepoint - datetime.now()).total_seconds()))
            result = next_task()
            # if False is returned - task is not repeated
            if result != False:
                self.add(
                    next_task.func,
                    next_task.timepoint + timedelta(seconds=next_task.frequency),
                    next_task.frequency,
                    *next_task.args,
                    **next_task.kwargs,
                )

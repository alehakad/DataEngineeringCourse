from typing import Callable, Generator, Any
from datetime import datetime, timedelta
from priority_queue import PriorityQueue
import time
from types import GeneratorType


class Scheduler:
    """
    class for scheduler of tasks:
    - tasks are chosen by earliest start time
    - tasks yield the time of next pause
    - if False is yielded, task is stopped
    """

    class SchedulerTask:
        def __init__(self, gen_object, timepoint):
            self.gen_object = gen_object
            self.timepoint = timepoint

        def __lt__(self, other: "Scheduler.SchedulerTask") -> bool:
            return self.timepoint < other.timepoint

        def __call__(self):
            try:
                return next(self.gen_object)
            except StopIteration:
                return False

    def __init__(self):
        self.task_queue = PriorityQueue()
        self.immediate_tasks_queue = []

    def add(
        self,
        task: Callable[..., Any] | Generator[Any, Any, Any],
        timepoint: datetime,
        *args,
        **kwargs
    ):
        if isinstance(task, GeneratorType):
            gen_object = task
        else:

            def function_wrapper():
                yield task(*args, **kwargs)

            gen_object = function_wrapper()

        self.task_queue.push(Scheduler.SchedulerTask(gen_object, timepoint))

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

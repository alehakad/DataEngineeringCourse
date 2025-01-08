from scheduler import Scheduler
from datetime import datetime, timedelta


def one_time_task(string: str):
    print(string)
    raise StopIteration


def returning_n_times_task(name: str):
    print(f"Hello, {name}!", datetime.now())
    yield


def test_scheduler_one_time_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(one_time_task, test_time, 0.5, "Hello")
    pq.run()


def test_scheduler_repeating_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(returning_n_times_task, test_time, 1, "World")
    pq.run()


if __name__ == "__main__":
    test_scheduler_one_time_tasks()
    test_scheduler_repeating_tasks()

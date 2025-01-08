from scheduler import Scheduler
from datetime import datetime, timedelta


def one_time_task(string: str):
    print(string)
    raise StopIteration


def returning_n_times_task(name: str):
    print(f"Hello, {name}!", datetime.now())
    yield 1

def returning_n_times_task2(name: str):
    print(f"Goodbuy, {name}!", datetime.now())
    yield 2


def test_scheduler_one_time_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(one_time_task, test_time, "Hello")
    pq.run()


def test_scheduler_repeating_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(returning_n_times_task, test_time, "World")
    pq.add(returning_n_times_task2, test_time + timedelta(seconds=1), "Sir")
    pq.run()


if __name__ == "__main__":
    test_scheduler_one_time_tasks()
    test_scheduler_repeating_tasks()

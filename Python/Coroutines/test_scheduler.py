from scheduler import Scheduler
from datetime import datetime, timedelta


def one_time_task(string: str):
    print(string)
    yield 1


def returning_n_times_task(name: str, n_times: int):
    for i in range(n_times):
        print(f"Goodbuy, {name, i}!", datetime.now())
        yield 2


def function_task():
    print("Function task")


def test_scheduler_one_time_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(one_time_task("Hello"), test_time)
    pq.run()


def test_scheduler_repeating_tasks():
    pq = Scheduler()
    test_time = datetime.now()
    pq.add(returning_n_times_task("Sir", 5), test_time + timedelta(seconds=1))
    pq.add(function_task, test_time + timedelta(seconds=5))
    pq.run()


if __name__ == "__main__":
    test_scheduler_one_time_tasks()
    test_scheduler_repeating_tasks()

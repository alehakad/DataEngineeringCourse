from typing import Generator


# history keeper that keeps up to n elements
def history_keeper(n_tasks: int) -> Generator[list[int], int, None]:
    history_list = []
    while True:
        new_task = yield history_list
        if new_task is not None:
            if len(history_list) == n_tasks:
                history_list.pop(0)
            history_list.append(new_task)

if __name__ == "__main__":
    gen = history_keeper(3)
    print(next(gen))
    print(gen.send(1))
    print(gen.send(2))
    print(gen.send(3))
    print(gen.send(4))
    print(next(gen))


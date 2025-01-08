from typing import Any


class PriorityQueue:
    """
    Priority queue class, that maintains elements order
    Element with lower values have higher priority
    """

    def __init__(self):
        self.queue = []

    def push(self, new_task: Any) -> None:
        """
        Adds new task to priority queue

        Args:
            new_task (Any): The task to add to the queue
        """
        # find indx to insert
        insert_idx = 0
        while insert_idx < len(self.queue) and new_task > self.queue[insert_idx]:
            insert_idx += 1

        self.queue.insert(insert_idx, new_task)

    def pop(self) -> Any:
        """
        Removes and returns element with highest priority

        Returns:
            Any: The task with higest priority

        Raises:
            IndexError: If the queue is empty
        """
        if len(self.queue) != 0:
            return self.queue.pop(0)
        raise IndexError("Empty queue")

    def peek(self) -> Any:
        """
        Returns the highest priority task without removing it

        Returns:
            Any: The task with higest priority

        Raises:
             IndexError: If the queue is empty
        """
        if len(self.queue) != 0:
            return self.queue[0]
        raise IndexError("Empty queue")

    def __len__(self) -> int:
        """
        Returns length of priority queue

        Returns:
            int: The number of tasks in the queue
        """
        return len(self.queue)

    def is_empty(self) -> bool:
        """
        Checks if priority queue is empty

        Returns:
            bool: True if there are no tasks are in queue, False otherwise
        """
        return len(self.queue) == 0

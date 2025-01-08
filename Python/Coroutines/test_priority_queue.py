import pytest
from priority_queue import PriorityQueue


def test_pq_len():
    pq = PriorityQueue()
    assert len(pq) == 0
    for i in range(10):
        pq.push(i)
        assert len(pq) == i + 1


def test_pq_pop():
    pq = PriorityQueue()
    for i in range(10):
        pq.push(i)
    for i in range(10):
        assert pq.pop() == i


def test_pq_peek():
    pq = PriorityQueue()
    for i in range(10):
        pq.push(i)
        assert pq.peek() == 0


def test_pq_is_empty():
    pq = PriorityQueue()
    assert pq.is_empty() == True
    pq.push(1)
    assert pq.is_empty() == False
    pq.pop()
    assert pq.is_empty() == True

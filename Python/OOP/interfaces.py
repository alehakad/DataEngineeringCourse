from typing import Protocol, List


class SortStrategy(Protocol):
    def sort(self, data: List[int]) -> List[int]: ...


# Implementing specific strategies
class QuickSort:
    def sort(self, data: List[int]) -> List[int]:
        print("Using QuickSort")
        return sorted(data)  # Simplified for the example


class BubbleSort:
    def sort(self, data: List[float]) -> List[int]:
        print("Using BubbleSort")
        for i in range(len(data)):
            for j in range(len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


# Function that works with any strategy conforming to SortStrategy
def perform_sorting(strategy: SortStrategy, data: List[int]) -> List[int]:
    return strategy.sort(data)


# Usage
data = [5, 2, 9, 1, 5, 6]

quick_sort = QuickSort()
bubble_sort = BubbleSort()

print(perform_sorting(quick_sort, data))  # Works because QuickSort has `sort`
print(perform_sorting(bubble_sort, data))  # Works because BubbleSort has `sort`
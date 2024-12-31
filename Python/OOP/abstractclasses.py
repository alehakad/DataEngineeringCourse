from abc import ABC, abstractmethod


# abstract classes in python
class Animal(ABC):
    @abstractmethod
    def sound(self):
        print("default sound")

    @abstractmethod
    def describe(self):
        pass

    def eat(self):
        print("Eating")


class Dog(Animal):
    def sound(self):
        return super().sound()

    def describe(self):
        print("I am dog")


if __name__ == "__main__":
    # will result in type error
    # a = Animal()
    # a.sound()

    dog = Dog()
    dog.sound()
    dog.eat()
    dog.describe()

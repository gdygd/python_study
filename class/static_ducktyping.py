from typing import Protocol

class Speakable(Protocol):
    def speak(self) -> None:
        ...

class Dog:
    def speak(self):
        print("DogDog")

class Robot:
    def speak(self):
        print("botbot")

class Stone:
    def roll(self):
        pass
    def speak(self):
        print("rollroll")

def greet(obj: Speakable):
    obj.speak()

greet(Dog())
greet(Robot())
greet(Stone())
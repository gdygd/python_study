from abc import ABC, abstractmethod

class Speaker(ABC):
    @abstractmethod
    def speak(self):
        pass

class Person(Speaker):
    def speak(self):
        print("Hi!")

class Animal(Speaker):
    def speak(self):
        print("Grrr!")

# sp = Speaker()
p = Person()
a = Animal()

p.speak
a.speak

# sp = p
# sp.speak()
# sp = a
# sp.speak()
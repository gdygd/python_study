class Dog:
    def speak(self):
        print("Woof")
    def Lister(self):
        print("dog...")

class Robot:
    def speak(self):
        print("Beep!")

def greet(speaker):
    speaker.speak()

greet(Dog())
greet(Robot())
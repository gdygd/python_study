MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}



resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


maker = CoffeeMaker()
moneyMachine = MoneyMachine()

# def __init__(self, name, water, milk, coffee, cost):

while True:
    choice = input("What would you like? (espresso/latte/cappuccino):").lower()

    if choice == "off":
        break
    elif choice == "report":
        maker.report()
        moneyMachine.report()
    else:
        ingre = MENU[choice]["ingredients"]
        cost = MENU[choice]["cost"]
        menu = MenuItem(choice, ingre["water"], ingre["milk"], ingre["coffee"], cost)

        print(f"cost:{cost}")

        ok = maker.is_resource_sufficient(menu)
        if ok == True:
            moneyMachine.make_payment(cost)
            maker.make_coffee(menu)




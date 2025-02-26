MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
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

profit = 0.0

PENY = 1
NICKEL = 5
DIME = 10
QUARTER = 25

def print_report():
    print(f"Water: {resources["water"]}ml")
    print(f"Milk: {resources["milk"]}ml")
    print(f"Coffee: {resources["coffee"]}g")
    print(f"Money: ${profit}")

def check_resource(ingredient):
    if ingredient["water"] > resources["water"]:
        print("Sorry there is not enough water.")
        return False
    elif ingredient["milk"] > resources["milk"]:
        print("Sorry there is not enough milk.")
        return False
    elif ingredient["coffee"] > resources["coffee"]:
        print("Sorry there is not enough coffee.")
        return False

    return True

def reduce_water(ingredient):
    return resources["water"] - ingredient["water"]
def reduce_milk(ingredient):
    return resources["milk"] - ingredient["milk"]
def reduce_coffee(ingredient):
    return resources["coffee"] - ingredient["coffee"]


def check_coin(q, d, n, p, cost):
    total = (p + (n*NICKEL) + (d*DIME) + (q*QUARTER)) / 100.0

    if total < cost:
        print("Sorry that's not enouth money. Money refunded.")
        return

    return round((total - cost), 1)


def get_cost(drink):
    return MENU[drink]["cost"]

def order_drink(choice):

    isok = check_resource(MENU[choice]["ingredients"])
    if isok == False:
        return False


    print("Please insert coins.")
    q = int(input("how many quarters?:"))
    d = int(input("how many dimes?:"))
    n = int(input("how many nickles?:"))
    p = int(input("how many pennies?:"))

    remain = check_coin(q, d, n, p, get_cost(choice))
    print(f"Here is ${remain} in change.")
    print(f"Here is your {choice} Enjoy!")

    return True



while True:
    choice = input("What would you like? (espresso/latte/cappuccino):").lower()
    if choice == "report":
        print_report()
    else:
        ok = order_drink(choice)
        if ok == True:
            profit += get_cost(choice)
            resources["water"] = reduce_water(MENU[choice]["ingredients"])
            resources["milk"] = reduce_milk(MENU[choice]["ingredients"])
            resources["coffee"] = reduce_coffee(MENU[choice]["ingredients"])








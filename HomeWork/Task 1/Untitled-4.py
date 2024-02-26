try:
    hours = float(input("Enter Hours: "))
    rate = float(input("Enter Rate: "))
    bonus = 1.25

    if hours <= 40:
        pay = hours * rate
        print("Your salary is:", pay, "EUR")
    else:
        pay =  40 * rate + (hours - 40) * rate * 1.25
        print("Your salary is:", pay, "EUR")
except ValueError:
    print("Please insert valid numbers.")


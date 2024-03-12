def compute_wage(hours, rate):
    regular_hours = min(hours, 40)
    overtime_hours = max(hours - 40, 0)
    pay = regular_hours * rate + overtime_hours * rate * 1.25
    return pay

hours = float(input("Enter Hours: "))
rate = float(input("Enter Rate: "))
pay = compute_wage(hours, rate)
print("Pay:", pay)
# tracker.py
# By siddharth
# Date: 2025-11-10
# Project Title: Meal Calorie Tracker


print("Welcome to the Meal Calorie Tracker!")
print("This tool helps you log your meals and calories, calculates your total and average intake, compares against your daily calorie limit, and generates a summary report.\n")

# Input & Data Collection
meal_names = []
calorie_amounts = []

meal_count_input = input("How many meals do you want to log today? ")
if not meal_count_input.isdigit():
    print("Invalid input. Please enter a whole number for meal count.")
    exit()
meal_count = int(meal_count_input)

for i in range(meal_count):
    name = input(f"Enter name for meal #{i+1} (e.g., Breakfast): ")
    cal_input = input(f"Enter calorie amount for {name}: ")
   
    calories = float(cal_input)
    
        
    meal_names.append(name)
    calorie_amounts.append(calories)

# Calorie Calculations
total_calories = sum(calorie_amounts)
average_calories = total_calories / meal_count if meal_count > 0 else 0

limit_input = input("Enter your daily calorie limit: ")
try:
    calorie_limit = float(limit_input)
except ValueError:
    print("Please enter a valid calorie number (e.g., 1800).")
    exit()

within_limit = total_calories <= calorie_limit

# Exceed Limit Warning System
if total_calories > calorie_limit:
    status_message = f"WARNING: You have exceeded your daily calorie limit by {total_calories - calorie_limit:.2f} calories."
else:
    status_message = f"Great job! You are within your daily calorie limit by {calorie_limit - total_calories:.2f} calories."

# Neatly Formatted Output
print("\nMeal Name\tCalories")
print("-" * 32)
for name, cal in zip(meal_names, calorie_amounts):
    print(f"{name:<15}\t{cal:.2f}")
print("-" * 32)
print(f"Total:\t\t{total_calories:.2f}")
print(f"Average:\t{average_calories:.2f}")
print(status_message)


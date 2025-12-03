
# GradeBook Analyzer
# Author: Siddharth Singh Kathait
# Date: 03 Dec 2025
# Purpose: Analyse and report student grades from input or CSV


import csv
import statistics


#Menu


def print_menu():
    print("\n===== GRADEBOOK ANALYZER =====")        
    print("1. Enter student data manually")
    print("2. Load student data from CSV")
    print("3. Exit")
    print("==============================")


#Data Input


def manual_input():                              
    marks = {}
    n = int(input("How many students? "))

    for _ in range(n):
        name = input("Enter student name: ")
        score = float(input(f"Enter marks for {name}: "))
        marks[name] = score

    return marks


def load_from_csv():                       
    filename = input("Enter CSV filename (example: marks.csv): ")

    marks = {}
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                name = row[0]
                score = float(row[1])
                marks[name] = score
        print("CSV loaded successfully!")
    except FileNotFoundError:               
        print("File not found!")
    except Exception as e:
        print("Error:", e)

    return marks


#Statistical Functions


def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)      


def calculate_median(marks_dict):     
    return statistics.median(marks_dict.values())


def find_max_score(marks_dict):   
    max_name = max(marks_dict, key=marks_dict.get)
    return max_name, marks_dict[max_name]


def find_min_score(marks_dict):    
    min_name = min(marks_dict, key=marks_dict.get)
    return min_name, marks_dict[min_name]


#Grade Assignment


def assign_grades(marks):      
    grades = {}
    for name, score in marks.items():
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        elif score >= 40:
            grade = "E"
        else:
            grade = "F"

        grades[name] = grade
    return grades


def grade_distribution(grades):  
    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    for g in grades.values():
        dist[g] += 1
    return dist


# Pass/Fail


def pass_fail_lists(marks):      
    passed = [name for name, score in marks.items() if score >= 40] 
    failed = [name for name, score in marks.items() if score < 40]
    return passed, failed


#Formatted Table


def print_table(marks, grades):    
    print("\nName\t\tMarks\tGrade")
    print("--------------------------------------")
    for name in marks:
        print(f"{name:12}\t{marks[name]:<6}\t{grades[name]}")
    print("--------------------------------------")


def export_csv(marks, grades):       
    filename = "studentgrades.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Marks", "Grade"])
        for name in marks:
            writer.writerow([name, marks[name], grades[name]])
    print(f"Results exported to {filename}")






def main():    
    while True:
        print_menu()
        choice = input("Choose an option (1–3): ")

        if choice == "1":   
            marks = manual_input()

        elif choice == "2": 
            marks = load_from_csv()
            if not marks:
                continue

        elif choice == "3":   
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice.")
            continue

       
        avg = calculate_average(marks)
        med = calculate_median(marks)
        max_name, max_score = find_max_score(marks)
        min_name, min_score = find_min_score(marks)

        grades = assign_grades(marks)
        dist = grade_distribution(grades)
        passed, failed = pass_fail_lists(marks)

        #results
        print("\n----- STATISTICAL SUMMARY -----")
        print(f"Average Score: {avg:.2f}")
        print(f"Median Score:  {med:.2f}")
        print(f"Highest Score: {max_name} ({max_score})")
        print(f"Lowest Score:  {min_name} ({min_score})")

        print("\n----- GRADE DISTRIBUTION -----")
        for grade, count in dist.items():
            print(f"{grade}: {count}")

        print("\n----- PASS / FAIL -----")
        print(f"Passed ({len(passed)}): {passed}")
        print(f"Failed ({len(failed)}): {failed}")

        print_table(marks, grades)

       
        exp = input("Do you want to export results to CSV? (y/n): ")
        if exp.lower() == "y":
            export_csv(marks, grades)


# Run program
if __name__ == "__main__":
    main()
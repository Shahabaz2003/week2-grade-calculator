# ==========================================
# Program: Student Grade Calculator
# Course: Week 2 - Control Flow & Data Structures
# Author: [Aapka Naam Yahan Likho]
# Description: Multi-student grading system with CLI colors and file export.
# ==========================================

"""
Program: Student Grade Calculator (Enhanced)
Course: Week 2 - Control Flow & Data Structures
Author: [Aapka Naam]
Description: Ek badhiya grading system jo multi-student data process karta hai,
             statistics nikalta hai, search aur file saving features ke sath.
"""

import sys

# Terminal ke liye Color Codes (ANSI Escape Sequences)
CLR_HEADER = '\033[95m'
CLR_BLUE = '\033[94m'
CLR_GREEN = '\033[92m'
CLR_YELLOW = '\033[93m'
CLR_RED = '\033[91m'
CLR_END = '\033[0m'
CLR_BOLD = '\033[1m'

def color_grade(grade):
    """Grade ke hisaab se color return karta hai"""
    if grade == 'A': return f"{CLR_GREEN}{CLR_BOLD}{grade}{CLR_END}"
    elif grade in ['B', 'C']: return f"{CLR_BLUE}{grade}{CLR_END}"
    elif grade == 'D': return f"{CLR_YELLOW}{grade}{CLR_END}"
    else: return f"{CLR_RED}{CLR_BOLD}{grade}{CLR_END}"

def calculate_grade(average):
    """Average ke hisaab se Grade aur Comment decide karta hai"""
    if average >= 90:
        return 'A', 'Excellent! Keep up the great work!'
    elif average >= 80:
        return 'B', "Very Good! You're doing well."
    elif average >= 70:
        return 'C', 'Good. Room for improvement.'
    elif average >= 60:
        return 'D', 'Needs Improvement. Please study more.'
    else:
        return 'F', 'Failed. Please seek help from your teacher.'

def get_valid_number(prompt, min_val=0.0, max_val=100.0, is_int=False):
    """Try-Except loop use karke galat input ko handle karta hai"""
    while True:
        try:
            user_input = input(prompt)
            if user_input.strip().lower() == 'exit':
                return None
                
            value = int(user_input) if is_int else float(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"{CLR_RED}Error: Please enter a number between {min_val} and {max_val}.{CLR_END}")
        except ValueError:
            print(f"{CLR_RED}Invalid input! Please enter a valid numerical value.{CLR_END}")

def process_new_students():
    """Students ka data collect karne ke liye function"""
    print(f"\n{CLR_HEADER}=== DATA COLLECTION ==={CLR_END}")
    num_students = get_valid_number("Enter number of students to add: ", min_val=1, max_val=100, is_int=True)
    if not num_students: return []

    new_batch = []
    for i in range(int(num_students)):
        print(f"\n--- Student {i+1} of {int(num_students)} ---")
        name = input("Student Name: ").strip()
        while not name:
            print(f"{CLR_RED}Name field cannot be left blank.{CLR_END}")
            name = input("Student Name: ").strip()
            
        print("Enter scores (0-100):")
        math = get_valid_number("  Math: ")
        science = get_valid_number("  Science: ")
        english = get_valid_number("  English: ")
        
        avg = (math + science + english) / 3
        grade, comment = calculate_grade(avg)
        
        student_data = {
            'name': name,
            'marks': [math, science, english],
            'average': round(avg, 1),
            'grade': grade,
            'comment': comment
        }
        new_batch.append(student_data)
    return new_batch

def display_summary(students):
    """Saare students ka result table format me dikhata hai"""
    if not students:
        print(f"{CLR_YELLOW}No records available to display.{CLR_END}")
        return
        
    print(f"\n{CLR_BOLD}{'='*75}{CLR_END}")
    print(f"{CLR_BOLD}                           STUDENT RESULTS SUMMARY{CLR_END}")
    print(f"{CLR_BOLD}{'='*75}{CLR_END}")
    print(f"{'Name':<20} | {'Avg':>5} | {'Grade':^5} | {'Feedback Note'}")
    print("-" * 75)
    
    for s in students:
        colored_g = color_grade(s['grade'])
        print(f"{s['name']:<20} | {s['average']:>5.1f} |   {colored_g}   | {s['comment']}")
    print("-" * 75)

def display_statistics(students):
    """Puri class ki stats (Highest, Lowest, Average) nikalta hai"""
    if not students: return
    
    avgs = [s['average'] for s in students]
    class_avg = sum(avgs) / len(avgs)
    
    highest_student = max(students, key=lambda x: x['average'])
    lowest_student = min(students, key=lambda x: x['average'])
    
    print(f"\n{CLR_HEADER}📈 CLASS STATISTICS{CLR_END}")
    print(f"  • Total Enrolled   : {len(students)}")
    print(f"  • Class Average    : {class_avg:.1f}")
    print(f"  • Highest Record   : {highest_student['average']:.1f} ({highest_student['name']})")
    print(f"  • Lowest Record    : {lowest_student['average']:.1f} ({lowest_student['name']})")
    print(f"{CLR_BOLD}{'='*75}{CLR_END}")

def search_student(students):
    """Student ka naam search karne ke liye feature"""
    if not students:
        print(f"{CLR_YELLOW}Database empty. Cannot execute search operations.{CLR_END}")
        return
    
    query = input("\nEnter student name to look up: ").strip().lower()
    found = [s for s in students if query in s['name'].lower()]
    
    if found:
        print(f"\n{CLR_GREEN}Found {len(found)} match(es):{CLR_END}")
        display_summary(found)
    else:
        print(f"{CLR_RED}No records match the query: '{query}'{CLR_END}")

def save_to_file(students, filename="results_sample.txt"):
    """Results ko text file me permanently save karta hai"""
    if not students:
        print(f"{CLR_YELLOW}No data found to export.{CLR_END}")
        return
    try:
        with open(filename, 'w') as f:
            f.write("=== STUDENT GRADE REPORT GENERATED EXPORT ===\n\n")
            f.write(f"{'Name':<20} | {'Avg':>5} | {'Grade':^5} | Comment\n")
            f.write("-" * 70 + "\n")
            for s in students:
                f.write(f"{s['name']:<20} | {s['average']:>5.1f} |   {s['grade']}   | {s['comment']}\n")
        print(f"{CLR_GREEN}✓ Successfully saved data to '{filename}'!{CLR_END}")
    except IOError as e:
        print(f"{CLR_RED}File write failed: {e}{CLR_END}")
def main():
    # Saara data store karne ke liye list
    student_database = []
    
    while True:
        print(f"\n{CLR_BOLD}--- METRIC GRADE ENGINE v2.0 ---{CLR_END}")
        print("1. Input New Student Data Batch")
        print("2. Display Report Card Matrix")
        print("3. Query / Search Registry")
        print("4. Save Report Card Data to Disk File")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            student_database.extend(process_new_students())
        elif choice == '2':
            display_summary(student_database)
            display_statistics(student_database)
        elif choice == '3':
            search_student(student_database)
        elif choice == '4':
            save_to_file(student_database)
        elif choice == '5':
            print(f"\n{CLR_BLUE}Exiting program. Goodbye!{CLR_END}")
            sys.exit()
        else:
            print(f"{CLR_RED}Invalid selection. Try options 1 through 5.{CLR_END}")

if __name__ == "__main__":
    main()
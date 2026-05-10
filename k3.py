# =========================================================
#                 GRADEBOOK APPLICATION
#         Student Grade Management System
# =========================================================

# Features:
# ✔ Add Student
# ✔ Add Marks
# ✔ Calculate GPA (Out of 10)
# ✔ Search Student
# ✔ Delete Student
# ✔ Export Report Card
# ✔ Beautiful GUI
# ✔ Table Display
# ✔ Performance Tracking

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("GradeBook - Student Grade Management System")

root.geometry("1000x650")

root.config(bg="#f4f6f9")

root.resizable(False, False)

# =========================================================
# DATA STORAGE
# =========================================================

students = {}

# =========================================================
# FUNCTIONS
# =========================================================

# ---------------------------------------------------------
# CLEAR INPUT FIELDS
# ---------------------------------------------------------

def clear_fields():

    name_entry.delete(0, tk.END)

    roll_entry.delete(0, tk.END)

    class_entry.delete(0, tk.END)

    subject_entry.delete(0, tk.END)

    marks_entry.delete(0, tk.END)


# ---------------------------------------------------------
# GRADE CALCULATION
# ---------------------------------------------------------

def get_grade(score):

    if score >= 90:
        return "A+"

    elif score >= 80:
        return "A"

    elif score >= 70:
        return "B"

    elif score >= 60:
        return "C"

    elif score >= 50:
        return "D"

    else:
        return "F"


# ---------------------------------------------------------
# GPA CALCULATION (OUT OF 10)
# ---------------------------------------------------------

def calculate_gpa(avg):

    if avg >= 90:
        return 10.0

    elif avg >= 80:
        return 9.0

    elif avg >= 70:
        return 8.0

    elif avg >= 60:
        return 7.0

    elif avg >= 50:
        return 6.0

    elif avg >= 40:
        return 5.0

    else:
        return 4.0


# ---------------------------------------------------------
# ADD STUDENT
# ---------------------------------------------------------

def add_student():

    name = name_entry.get().strip()

    roll = roll_entry.get().strip()

    class_name = class_entry.get().strip()

    subject = subject_entry.get().strip()

    marks = marks_entry.get().strip()

    # Validation

    if name == "" or roll == "" or class_name == "":
        messagebox.showerror(
            "Error",
            "Please fill all required fields"
        )
        return

    if subject == "":
        messagebox.showerror(
            "Error",
            "Please enter subject"
        )
        return

    try:
        marks = float(marks)

    except:
        messagebox.showerror(
            "Error",
            "Marks must be number"
        )
        return

    if marks < 0 or marks > 100:
        messagebox.showerror(
            "Error",
            "Marks must be between 0 and 100"
        )
        return

    # Add Student

    if name not in students:

        students[name] = {

            "roll": roll,

            "class": class_name,

            "subjects": {}

        }

    students[name]["subjects"][subject] = marks

    messagebox.showinfo(
        "Success",
        "Student Added Successfully"
    )

    clear_fields()

    show_students()


# ---------------------------------------------------------
# SHOW STUDENTS IN TABLE
# ---------------------------------------------------------

def show_students():

    table.delete(*table.get_children())

    for name, data in students.items():

        subjects = data["subjects"]

        total = sum(subjects.values())

        average = total / len(subjects)

        grade = get_grade(average)

        gpa = calculate_gpa(average)

        table.insert(

            "",

            tk.END,

            values=(

                name,

                data["roll"],

                data["class"],

                len(subjects),

                round(average, 2),

                grade,

                gpa

            )
        )


# ---------------------------------------------------------
# SEARCH STUDENT
# ---------------------------------------------------------

def search_student():

    search_name = search_entry.get().lower()

    table.delete(*table.get_children())

    for name, data in students.items():

        if search_name in name.lower():

            subjects = data["subjects"]

            total = sum(subjects.values())

            average = total / len(subjects)

            grade = get_grade(average)

            gpa = calculate_gpa(average)

            table.insert(

                "",

                tk.END,

                values=(

                    name,

                    data["roll"],

                    data["class"],

                    len(subjects),

                    round(average, 2),

                    grade,

                    gpa

                )
            )


# ---------------------------------------------------------
# DELETE STUDENT
# ---------------------------------------------------------

def delete_student():

    selected = table.selection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Please select student"
        )

        return

    item = table.item(selected)

    student_name = item["values"][0]

    confirm = messagebox.askyesno(
        "Confirm",
        f"Delete {student_name}?"
    )

    if confirm:

        del students[student_name]

        show_students()

        messagebox.showinfo(
            "Deleted",
            "Student Deleted Successfully"
        )


# ---------------------------------------------------------
# EXPORT REPORT CARD
# ---------------------------------------------------------

def export_report():

    selected = table.selection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Please select student"
        )

        return

    item = table.item(selected)

    name = item["values"][0]

    data = students[name]

    subjects = data["subjects"]

    total = sum(subjects.values())

    average = total / len(subjects)

    grade = get_grade(average)

    gpa = calculate_gpa(average)

    filename = name.replace(" ", "_") + "_Report.txt"

    file = open(filename, "w")

    file.write("=" * 50 + "\n")

    file.write("          GRADEBOOK REPORT CARD\n")

    file.write("=" * 50 + "\n\n")

    file.write(f"Student Name : {name}\n")

    file.write(f"Roll Number  : {data['roll']}\n")

    file.write(f"Class        : {data['class']}\n")

    file.write(f"Date         : {datetime.date.today()}\n")

    file.write("\n")

    file.write("-" * 50 + "\n")

    file.write("{:<20} {:<10}\n".format(
        "Subject",
        "Marks"
    ))

    file.write("-" * 50 + "\n")

    for subject, marks in subjects.items():

        file.write("{:<20} {:<10}\n".format(
            subject,
            marks
        ))

    file.write("-" * 50 + "\n")

    file.write(f"Average : {round(average,2)}\n")

    file.write(f"Grade   : {grade}\n")

    file.write(f"GPA     : {gpa}/10\n")

    file.write("\n")

    if gpa >= 9:
        file.write("Performance : Excellent\n")

    elif gpa >= 7:
        file.write("Performance : Very Good\n")

    elif gpa >= 6:
        file.write("Performance : Good\n")

    else:
        file.write("Performance : Needs Improvement\n")

    file.write("\n")

    file.write("=" * 50)

    file.close()

    messagebox.showinfo(
        "Success",
        f"Report Exported as {filename}"
    )


# =========================================================
# TITLE SECTION
# =========================================================

title = tk.Label(

    root,

    text="GradeBook",

    font=("Arial", 28, "bold"),

    bg="#f4f6f9",

    fg="#2563eb"

)

title.pack(pady=10)

subtitle = tk.Label(

    root,

    text="Student Grade Management System",

    font=("Arial", 12),

    bg="#f4f6f9",

    fg="gray"

)

subtitle.pack()

# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.Frame(

    root,

    bg="white",

    bd=2,

    relief=tk.RIDGE

)

form_frame.pack(

    pady=15,

    padx=20,

    fill="x"

)

# =========================================================
# NAME
# =========================================================

tk.Label(

    form_frame,

    text="Student Name",

    font=("Arial", 11),

    bg="white"

).grid(row=0, column=0, padx=10, pady=10)

name_entry = tk.Entry(

    form_frame,

    font=("Arial", 11),

    width=25

)

name_entry.grid(row=0, column=1)

# =========================================================
# ROLL NUMBER
# =========================================================

tk.Label(

    form_frame,

    text="Roll Number",

    font=("Arial", 11),

    bg="white"

).grid(row=0, column=2, padx=10)

roll_entry = tk.Entry(

    form_frame,

    font=("Arial", 11),

    width=25

)

roll_entry.grid(row=0, column=3)

# =========================================================
# CLASS
# =========================================================

tk.Label(

    form_frame,

    text="Class",

    font=("Arial", 11),

    bg="white"

).grid(row=1, column=0, padx=10, pady=10)

class_entry = tk.Entry(

    form_frame,

    font=("Arial", 11),

    width=25

)

class_entry.grid(row=1, column=1)

# =========================================================
# SUBJECT
# =========================================================

tk.Label(

    form_frame,

    text="Subject",

    font=("Arial", 11),

    bg="white"

).grid(row=1, column=2)

subject_entry = tk.Entry(

    form_frame,

    font=("Arial", 11),

    width=25

)

subject_entry.grid(row=1, column=3)

# =========================================================
# MARKS
# =========================================================

tk.Label(

    form_frame,

    text="Marks",

    font=("Arial", 11),

    bg="white"

).grid(row=2, column=0, padx=10, pady=10)

marks_entry = tk.Entry(

    form_frame,

    font=("Arial", 11),

    width=25

)

marks_entry.grid(row=2, column=1)

# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(

    root,

    bg="#f4f6f9"

)

button_frame.pack(pady=10)

# ADD BUTTON

add_btn = tk.Button(

    button_frame,

    text="Add Student",

    font=("Arial", 11, "bold"),

    bg="#2563eb",

    fg="white",

    width=15,

    command=add_student

)

add_btn.grid(row=0, column=0, padx=10)

# DELETE BUTTON

delete_btn = tk.Button(

    button_frame,

    text="Delete Student",

    font=("Arial", 11, "bold"),

    bg="#dc2626",

    fg="white",

    width=15,

    command=delete_student

)

delete_btn.grid(row=0, column=1, padx=10)

# EXPORT BUTTON

export_btn = tk.Button(

    button_frame,

    text="Export Report",

    font=("Arial", 11, "bold"),

    bg="#059669",

    fg="white",

    width=15,

    command=export_report

)

export_btn.grid(row=0, column=2, padx=10)

# =========================================================
# SEARCH BAR
# =========================================================

search_frame = tk.Frame(

    root,

    bg="#f4f6f9"

)

search_frame.pack(pady=10)

search_entry = tk.Entry(

    search_frame,

    font=("Arial", 11),

    width=35

)

search_entry.grid(row=0, column=0, padx=10)

search_btn = tk.Button(

    search_frame,

    text="Search Student",

    font=("Arial", 10, "bold"),

    bg="#7c3aed",

    fg="white",

    command=search_student

)

search_btn.grid(row=0, column=1)

# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(root)

table_frame.pack(pady=20)

columns = (

    "Name",

    "Roll No",

    "Class",

    "Subjects",

    "Average",

    "Grade",

    "GPA"

)

table = ttk.Treeview(

    table_frame,

    columns=columns,

    show="headings",

    height=14

)

# TABLE HEADINGS

for col in columns:

    table.heading(col, text=col)

    table.column(col, width=130)

table.pack()

# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(

    root,

    text="GradeBook • Developed Using Python Tkinter",

    font=("Arial", 10),

    bg="#f4f6f9",

    fg="gray"

)

footer.pack(pady=10)

# =========================================================
# RUN APPLICATION
# =========================================================

root.mainloop()
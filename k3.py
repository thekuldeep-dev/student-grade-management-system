# =========================================================
# STUDENT GRADE MANAGEMENT SYSTEM WITH SIMPLE GUI
# Python Tkinter Project
# =========================================================

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("Student Grade Management System")

root.geometry("900x600")

root.config(bg="#f0f4f7")

# =========================================================
# DATA STORAGE
# =========================================================

students = {}

# =========================================================
# FUNCTIONS
# =========================================================

def get_grade(score):

    if score >= 90:
        return "A"

    elif score >= 75:
        return "B"

    elif score >= 60:
        return "C"

    elif score >= 40:
        return "D"

    else:
        return "F"


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


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    name = name_entry.get()

    roll = roll_entry.get()

    class_name = class_entry.get()

    subject = subject_entry.get()

    marks = marks_entry.get()

    # Validation

    if name == "" or roll == "" or class_name == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        marks = float(marks)

    except:
        messagebox.showerror("Error", "Marks must be number")
        return

    if marks < 0 or marks > 100:
        messagebox.showerror("Error", "Marks must be between 0-100")
        return

    # Add Student

    if name not in students:

        students[name] = {
            "roll": roll,
            "class": class_name,
            "subjects": {}
        }

    students[name]["subjects"][subject] = marks

    messagebox.showinfo("Success", "Student Added Successfully")

    clear_fields()

    show_students()


# =========================================================
# SHOW STUDENTS
# =========================================================

def show_students():

    table.delete(*table.get_children())

    for name, data in students.items():

        subjects = data["subjects"]

        total = sum(subjects.values())

        average = total / len(subjects)

        grade = get_grade(average)

        gpa = calculate_gpa(average)

        table.insert("", tk.END, values=(

            name,
            data["roll"],
            data["class"],
            round(average, 2),
            grade,
            gpa

        ))


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    search_name = search_entry.get()

    table.delete(*table.get_children())

    for name, data in students.items():

        if search_name.lower() in name.lower():

            subjects = data["subjects"]

            total = sum(subjects.values())

            average = total / len(subjects)

            grade = get_grade(average)

            gpa = calculate_gpa(average)

            table.insert("", tk.END, values=(

                name,
                data["roll"],
                data["class"],
                round(average, 2),
                grade,
                gpa

            ))


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Select Student")
        return

    item = table.item(selected)

    name = item["values"][0]

    del students[name]

    messagebox.showinfo("Deleted", "Student Deleted")

    show_students()


# =========================================================
# EXPORT REPORT
# =========================================================

def export_report():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Select Student")
        return

    item = table.item(selected)

    name = item["values"][0]

    data = students[name]

    subjects = data["subjects"]

    total = sum(subjects.values())

    average = total / len(subjects)

    grade = get_grade(average)

    gpa = calculate_gpa(average)

    filename = name.replace(" ", "_") + "_report.txt"

    file = open(filename, "w")

    file.write("====================================\n")
    file.write("     STUDENT REPORT CARD\n")
    file.write("====================================\n\n")

    file.write(f"Name : {name}\n")
    file.write(f"Roll : {data['roll']}\n")
    file.write(f"Class : {data['class']}\n\n")

    file.write("------------------------------------\n")

    for subject, marks in subjects.items():

        file.write(f"{subject} : {marks}\n")

    file.write("------------------------------------\n\n")

    file.write(f"Average : {round(average,2)}\n")

    file.write(f"Grade : {grade}\n")

    file.write(f"GPA : {gpa}\n")

    file.close()

    messagebox.showinfo("Success", f"Report Saved As {filename}")


# =========================================================
# CLEAR FIELDS
# =========================================================

def clear_fields():

    name_entry.delete(0, tk.END)

    roll_entry.delete(0, tk.END)

    class_entry.delete(0, tk.END)

    subject_entry.delete(0, tk.END)

    marks_entry.delete(0, tk.END)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(

    root,
    text="Student Grade Management System",
    font=("Arial", 22, "bold"),
    bg="#f0f4f7",
    fg="#1f2937"

)

title.pack(pady=15)

# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)

form_frame.pack(pady=10, padx=20, fill="x")

# =========================================================
# NAME
# =========================================================

name_label = tk.Label(

    form_frame,
    text="Student Name",
    font=("Arial", 12),
    bg="white"

)

name_label.grid(row=0, column=0, padx=10, pady=10)

name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)

name_entry.grid(row=0, column=1, padx=10, pady=10)

# =========================================================
# ROLL
# =========================================================

roll_label = tk.Label(

    form_frame,
    text="Roll Number",
    font=("Arial", 12),
    bg="white"

)

roll_label.grid(row=0, column=2, padx=10, pady=10)

roll_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)

roll_entry.grid(row=0, column=3, padx=10, pady=10)

# =========================================================
# CLASS
# =========================================================

class_label = tk.Label(

    form_frame,
    text="Class",
    font=("Arial", 12),
    bg="white"

)

class_label.grid(row=1, column=0, padx=10, pady=10)

class_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)

class_entry.grid(row=1, column=1, padx=10, pady=10)

# =========================================================
# SUBJECT
# =========================================================

subject_label = tk.Label(

    form_frame,
    text="Subject",
    font=("Arial", 12),
    bg="white"

)

subject_label.grid(row=1, column=2, padx=10, pady=10)

subject_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)

subject_entry.grid(row=1, column=3, padx=10, pady=10)

# =========================================================
# MARKS
# =========================================================

marks_label = tk.Label(

    form_frame,
    text="Marks",
    font=("Arial", 12),
    bg="white"

)

marks_label.grid(row=2, column=0, padx=10, pady=10)

marks_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)

marks_entry.grid(row=2, column=1, padx=10, pady=10)

# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(root, bg="#f0f4f7")

button_frame.pack(pady=10)

# Add Button

add_btn = tk.Button(

    button_frame,
    text="Add Student",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    width=15,
    command=add_student

)

add_btn.grid(row=0, column=0, padx=10)

# Delete Button

delete_btn = tk.Button(

    button_frame,
    text="Delete Student",
    font=("Arial", 12, "bold"),
    bg="#dc2626",
    fg="white",
    width=15,
    command=delete_student

)

delete_btn.grid(row=0, column=1, padx=10)

# Export Button

export_btn = tk.Button(

    button_frame,
    text="Export Report",
    font=("Arial", 12, "bold"),
    bg="#059669",
    fg="white",
    width=15,
    command=export_report

)

export_btn.grid(row=0, column=2, padx=10)

# =========================================================
# SEARCH
# =========================================================

search_frame = tk.Frame(root, bg="#f0f4f7")

search_frame.pack(pady=10)

search_label = tk.Label(

    search_frame,
    text="Search Student",
    font=("Arial", 12),
    bg="#f0f4f7"

)

search_label.grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)

search_entry.grid(row=0, column=1, padx=5)

search_btn = tk.Button(

    search_frame,
    text="Search",
    font=("Arial", 11, "bold"),
    bg="#7c3aed",
    fg="white",
    command=search_student

)

search_btn.grid(row=0, column=2, padx=5)

# =========================================================
# TABLE
# =========================================================

table_frame = tk.Frame(root)

table_frame.pack(pady=20)

columns = (

    "Name",
    "Roll",
    "Class",
    "Average",
    "Grade",
    "GPA"

)

table = ttk.Treeview(

    table_frame,
    columns=columns,
    show="headings",
    height=12

)

# Headings

for col in columns:

    table.heading(col, text=col)

    table.column(col, width=130)

table.pack()

# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(

    root,
    text="Simple Python Tkinter Project",
    font=("Arial", 10),
    bg="#f0f4f7",
    fg="gray"

)

footer.pack(pady=10)

# =========================================================
# RUN PROGRAM
# =========================================================

root.mainloop()

# =========================================================
#                 GRADEBOOK WEB APPLICATION
#        Student Grade Management System (Flask)
# =========================================================

from flask import Flask, render_template_string, request, redirect, send_file
import datetime

app = Flask(__name__)

# =========================================================
# DATA STORAGE
# =========================================================

students = {}

# =========================================================
# HTML TEMPLATE
# =========================================================

HTML = """

<!DOCTYPE html>
<html>

<head>

    <title>GradeBook</title>

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:Arial;
        }

        body{
            background:#0f172a;
            color:white;
        }

        /* NAVBAR */

        .navbar{
            background:#111827;
            padding:20px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            box-shadow:0px 0px 10px black;
        }

        .logo{
            font-size:32px;
            font-weight:bold;
            color:#60a5fa;
        }

        .subtitle{
            color:lightgray;
            font-size:14px;
        }

        /* MAIN */

        .container{
            width:92%;
            margin:auto;
            margin-top:25px;
        }

        /* ANALYSIS */

        .analysis{
            display:grid;
            grid-template-columns:1fr 1fr 1fr;
            gap:20px;
            margin-bottom:25px;
        }

        .box{
            background:#1e293b;
            padding:25px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 0px 10px rgba(0,0,0,0.4);
        }

        .box h1{
            color:#60a5fa;
            margin-bottom:10px;
        }

        /* CARD */

        .card{
            background:#1e293b;
            padding:25px;
            border-radius:15px;
            margin-bottom:25px;
            box-shadow:0px 0px 15px rgba(0,0,0,0.4);
        }

        .card h2{
            color:#60a5fa;
            margin-bottom:20px;
        }

        /* FORM */

        .form-grid{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:15px;
        }

        input{
            padding:12px;
            border:none;
            border-radius:8px;
            background:#334155;
            color:white;
            outline:none;
        }

        input::placeholder{
            color:#cbd5e1;
        }

        /* BUTTON */

        button{
            background:#2563eb;
            color:white;
            border:none;
            padding:12px 18px;
            border-radius:8px;
            margin-top:15px;
            cursor:pointer;
            font-weight:bold;
            transition:0.3s;
        }

        button:hover{
            background:#1d4ed8;
            transform:scale(1.03);
        }

        .delete-btn{
            background:#dc2626;
        }

        .delete-btn:hover{
            background:#b91c1c;
        }

        .report-btn{
            background:#059669;
        }

        .report-btn:hover{
            background:#047857;
        }

        /* TABLE */

        table{
            width:100%;
            border-collapse:collapse;
            margin-top:20px;
        }

        th{
            background:#2563eb;
            padding:14px;
        }

        td{
            background:#1e293b;
            padding:14px;
            text-align:center;
            border-bottom:1px solid #334155;
        }

        tr:hover td{
            background:#273549;
        }

        /* GPA */

        .gpa{
            background:#059669;
            padding:6px 12px;
            border-radius:20px;
            font-weight:bold;
        }

        /* FOOTER */

        .footer{
            text-align:center;
            padding:20px;
            color:gray;
        }

        /* RESPONSIVE */

        @media(max-width:800px){

            .analysis{
                grid-template-columns:1fr;
            }

            .form-grid{
                grid-template-columns:1fr;
            }

            table{
                font-size:12px;
            }

        }

    </style>

</head>

<body>

    <!-- NAVBAR -->

    <div class="navbar">

        <div>

            <div class="logo">
                GradeBook
            </div>

            <div class="subtitle">
                Student Grade Management System
            </div>

        </div>

    </div>

    <!-- MAIN -->

    <div class="container">

        <!-- ANALYSIS -->

        <div class="analysis">

            <div class="box">

                <h1>{{ total_students }}</h1>

                <p>Total Students</p>

            </div>

            <div class="box">

                <h1>{{ average_gpa }}</h1>

                <p>Average GPA</p>

            </div>

            <div class="box">

                <h1>{{ topper }}</h1>

                <p>Top Performer</p>

            </div>

        </div>

        <!-- FORM -->

        <div class="card">

            <h2>Add Student Marks</h2>

            <form method="POST" action="/add">

                <div class="form-grid">

                    <input type="text"
                    name="name"
                    placeholder="Student Name"
                    required>

                    <input type="text"
                    name="roll"
                    placeholder="Roll Number"
                    required>

                    <input type="text"
                    name="class_name"
                    placeholder="Class"
                    required>

                    <input type="text"
                    name="subject"
                    placeholder="Subject Name"
                    required>

                    <input type="number"
                    name="marks"
                    placeholder="Marks"
                    required>

                </div>

                <button type="submit">

                    Add Subject

                </button>

            </form>

        </div>

        <!-- TABLE -->

        <div class="card">

            <h2>Student Records</h2>

            <table>

                <tr>

                    <th>Name</th>
                    <th>Roll</th>
                    <th>Class</th>
                    <th>Subjects & Marks</th>
                    <th>Average</th>
                    <th>Grade</th>
                    <th>GPA</th>
                    <th>Performance</th>
                    <th>Action</th>

                </tr>

                {% for student in students %}

                <tr>

                    <td>{{ student.name }}</td>

                    <td>{{ student.roll }}</td>

                    <td>{{ student.class_name }}</td>

                    <td>{{ student.subjects|safe }}</td>

                    <td>{{ student.average }}</td>

                    <td>{{ student.grade }}</td>

                    <td>

                        <span class="gpa">

                            {{ student.gpa }}/10

                        </span>

                    </td>

                    <td>{{ student.performance }}</td>

                    <td>

                        <a href="/report/{{ student.name }}">

                            <button class="report-btn">

                                Report

                            </button>

                        </a>

                        <a href="/delete/{{ student.name }}">

                            <button class="delete-btn">

                                Delete

                            </button>

                        </a>

                    </td>

                </tr>

                {% endfor %}

            </table>

        </div>

    </div>

    <!-- FOOTER -->

    <div class="footer">

        GradeBook • Developed Using Python Flask

    </div>

</body>

</html>

"""

# =========================================================
# GRADE FUNCTION
# =========================================================

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

# =========================================================
# GPA FUNCTION
# =========================================================

def calculate_gpa(score):

    if score >= 90:
        return 10

    elif score >= 80:
        return 9

    elif score >= 70:
        return 8

    elif score >= 60:
        return 7

    elif score >= 50:
        return 6

    else:
        return 5

# =========================================================
# PERFORMANCE FUNCTION
# =========================================================

def performance(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Very Good"

    elif score >= 60:
        return "Good"

    else:
        return "Needs Improvement"

# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")

def home():

    student_list = []

    total_gpa = 0

    topper = "None"

    highest_average = 0

    for name, data in students.items():

        subjects = data["subjects"]

        total_marks = sum(subjects.values())

        total_subjects = len(subjects)

        average = total_marks / total_subjects

        grade = get_grade(average)

        gpa = calculate_gpa(average)

        total_gpa += gpa

        if average > highest_average:

            highest_average = average

            topper = name

        # Subject display

        subject_text = ""

        for subject, marks in subjects.items():

            subject_text += f"{subject} ({marks}) <br>"

        student_list.append({

            "name": name,

            "roll": data["roll"],

            "class_name": data["class"],

            "subjects": subject_text,

            "average": round(average, 2),

            "grade": grade,

            "gpa": gpa,

            "performance": performance(average)

        })

    total_students = len(students)

    average_gpa = round(
        total_gpa / total_students,
        2
    ) if total_students > 0 else 0

    return render_template_string(

        HTML,

        students=student_list,

        total_students=total_students,

        average_gpa=average_gpa,

        topper=topper

    )

# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/add", methods=["POST"])

def add_student():

    name = request.form["name"]

    roll = request.form["roll"]

    class_name = request.form["class_name"]

    subject = request.form["subject"]

    marks = float(request.form["marks"])

    # Create student if not exists

    if name not in students:

        students[name] = {

            "roll": roll,

            "class": class_name,

            "subjects": {}

        }

    # Add multiple subjects

    students[name]["subjects"][subject] = marks

    return redirect("/")

# =========================================================
# DELETE STUDENT
# =========================================================

@app.route("/delete/<name>")

def delete_student(name):

    if name in students:

        del students[name]

    return redirect("/")

# =========================================================
# REPORT GENERATION
# =========================================================

@app.route("/report/<name>")

def report(name):

    if name not in students:

        return "Student Not Found"

    data = students[name]

    subjects = data["subjects"]

    total_marks = sum(subjects.values())

    average = total_marks / len(subjects)

    grade = get_grade(average)

    gpa = calculate_gpa(average)

    filename = name + "_Report.txt"

    with open(filename, "w") as file:

        file.write("=================================\n")

        file.write("       GRADEBOOK REPORT\n")

        file.write("=================================\n\n")

        file.write(f"Student Name : {name}\n")

        file.write(f"Roll Number  : {data['roll']}\n")

        file.write(f"Class        : {data['class']}\n\n")

        file.write("---------------------------------\n")

        file.write("Subjects & Marks\n")

        file.write("---------------------------------\n")

        for subject, marks in subjects.items():

            file.write(f"{subject} : {marks}\n")

        file.write("\n")

        file.write(f"Average : {round(average,2)}\n")

        file.write(f"Grade   : {grade}\n")

        file.write(f"GPA     : {gpa}/10\n")

        file.write(
            f"Performance : {performance(average)}\n"
        )

        file.write("\n")

        file.write(
            "Generated On : "
        )

        file.write(
            str(datetime.date.today())
        )

    return send_file(

        filename,

        as_attachment=True

    )

# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
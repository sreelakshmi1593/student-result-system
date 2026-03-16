from database import get_connection, calculate_grade

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Add Students
    students = [
        ("Priya Sharma", "CS001", "Computer Science", 2),
        ("Rahul Verma", "CS002", "Computer Science", 2),
        ("Anitha Reddy", "CS003", "Computer Science", 2),
        ("Kiran Kumar", "CS004", "Computer Science", 2),
        ("Divya Nair", "CS005", "Computer Science", 2),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO students (name, roll_number, department, year) VALUES (?, ?, ?, ?)",
        students
    )

    # Add Subjects
    subjects = [
        ("Mathematics", "MATH101", 100),
        ("Python Programming", "PY102", 100),
        ("Data Structures", "DS103", 100),
        ("Database Management", "DB104", 100),
        ("Web Technologies", "WT105", 100),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO subjects (name, code, max_marks) VALUES (?, ?, ?)",
        subjects
    )
    conn.commit()

    # Add Results
    marks_data = [
        ("CS001", "MATH101", 92), ("CS001", "PY102", 88),
        ("CS001", "DS103", 76), ("CS001", "DB104", 85),
        ("CS001", "WT105", 90),

        ("CS002", "MATH101", 65), ("CS002", "PY102", 72),
        ("CS002", "DS103", 58), ("CS002", "DB104", 70),
        ("CS002", "WT105", 68),

        ("CS003", "MATH101", 95), ("CS003", "PY102", 91),
        ("CS003", "DS103", 89), ("CS003", "DB104", 93),
        ("CS003", "WT105", 97),

        ("CS004", "MATH101", 45), ("CS004", "PY102", 52),
        ("CS004", "DS103", 48), ("CS004", "DB104", 55),
        ("CS004", "WT105", 50),

        ("CS005", "MATH101", 78), ("CS005", "PY102", 82),
        ("CS005", "DS103", 75), ("CS005", "DB104", 80),
        ("CS005", "WT105", 79),
    ]

    for roll, code, marks in marks_data:
        student = cursor.execute(
            "SELECT id FROM students WHERE roll_number=?", (roll,)
        ).fetchone()
        subject = cursor.execute(
            "SELECT id FROM subjects WHERE code=?", (code,)
        ).fetchone()
        if student and subject:
            grade = calculate_grade(marks)
            cursor.execute(
                "INSERT OR IGNORE INTO results (student_id, subject_id, marks_obtained, grade) VALUES (?, ?, ?, ?)",
                (student["id"], subject["id"], marks, grade)
            )

    conn.commit()
    conn.close()
    print("Sample data seeded successfully!")
    print("5 students, 5 subjects, 25 results added.")

if __name__ == "__main__":
    seed_data()

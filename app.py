from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection, calculate_grade, init_db

app = Flask(__name__)
CORS(app)

init_db()

# ── STUDENTS ─────────────────────────────────

@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_connection()
    students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(s) for s in students])

@app.route("/api/students/<int:id>", methods=["GET"])
def get_student(id):
    conn = get_connection()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data.get("name")
    roll_number = data.get("roll_number")
    department = data.get("department")
    year = data.get("year")
    if not all([name, roll_number, department, year]):
        return jsonify({"error": "All fields required"}), 400
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO students (name, roll_number, department, year) VALUES (?, ?, ?, ?)",
            (name, roll_number, department, year)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": "Roll number already exists"}), 400

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_connection()
    conn.execute("DELETE FROM results WHERE student_id=?", (id,))
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

# ── SUBJECTS ─────────────────────────────────

@app.route("/api/subjects", methods=["GET"])
def get_subjects():
    conn = get_connection()
    subjects = conn.execute("SELECT * FROM subjects ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(s) for s in subjects])

@app.route("/api/subjects", methods=["POST"])
def add_subject():
    data = request.get_json()
    name = data.get("name")
    code = data.get("code")
    max_marks = data.get("max_marks", 100)
    if not all([name, code]):
        return jsonify({"error": "Name and code required"}), 400
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO subjects (name, code, max_marks) VALUES (?, ?, ?)",
            (name, code, max_marks)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Subject added successfully"}), 201
    except:
        return jsonify({"error": "Subject code already exists"}), 400

# ── RESULTS ──────────────────────────────────

@app.route("/api/results", methods=["POST"])
def add_result():
    data = request.get_json()
    student_id = data.get("student_id")
    subject_id = data.get("subject_id")
    marks = data.get("marks_obtained")
    if not all([student_id, subject_id, marks is not None]):
        return jsonify({"error": "All fields required"}), 400
    if marks < 0 or marks > 100:
        return jsonify({"error": "Marks must be between 0 and 100"}), 400
    grade = calculate_grade(marks)
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO results (student_id, subject_id, marks_obtained, grade) VALUES (?, ?, ?, ?)",
            (student_id, subject_id, marks, grade)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Result added", "grade": grade}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/results/<int:student_id>", methods=["GET"])
def get_student_results(student_id):
    conn = get_connection()
    results = conn.execute("""
        SELECT results.id, subjects.name as subject, subjects.code,
               results.marks_obtained, results.grade, subjects.max_marks
        FROM results
        JOIN subjects ON results.subject_id = subjects.id
        WHERE results.student_id = ?
        ORDER BY subjects.name
    """, (student_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in results])

# ── REPORT ───────────────────────────────────

@app.route("/api/report/<int:student_id>", methods=["GET"])
def get_report(student_id):
    conn = get_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (student_id,)
    ).fetchone()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    results = conn.execute("""
        SELECT subjects.name as subject, subjects.code,
               results.marks_obtained, results.grade, subjects.max_marks
        FROM results
        JOIN subjects ON results.subject_id = subjects.id
        WHERE results.student_id = ?
        ORDER BY subjects.name
    """, (student_id,)).fetchall()
    conn.close()

    results_list = [dict(r) for r in results]
    if results_list:
        total = sum(r["marks_obtained"] for r in results_list)
        max_total = sum(r["max_marks"] for r in results_list)
        percentage = round((total / max_total) * 100, 2)
        overall_grade = calculate_grade(percentage)
    else:
        total = max_total = percentage = 0
        overall_grade = "N/A"

    return jsonify({
        "student": dict(student),
        "results": results_list,
        "total_marks": total,
        "max_marks": max_total,
        "percentage": percentage,
        "overall_grade": overall_grade
    })

@app.route("/api/report/all", methods=["GET"])
def get_all_reports():
    conn = get_connection()
    students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    conn.close()

    all_reports = []
    for student in students:
        conn = get_connection()
        results = conn.execute("""
            SELECT results.marks_obtained, subjects.max_marks
            FROM results
            JOIN subjects ON results.subject_id = subjects.id
            WHERE results.student_id = ?
        """, (student["id"],)).fetchall()
        conn.close()

        if results:
            total = sum(r["marks_obtained"] for r in results)
            max_total = sum(r["max_marks"] for r in results)
            percentage = round((total / max_total) * 100, 2)
            overall_grade = calculate_grade(percentage)
        else:
            percentage = 0
            overall_grade = "N/A"

        all_reports.append({
            "id": student["id"],
            "name": student["name"],
            "roll_number": student["roll_number"],
            "department": student["department"],
            "year": student["year"],
            "percentage": percentage,
            "overall_grade": overall_grade
        })

    return jsonify(all_reports)

# ── RUN ──────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5001)

# Student Result Management System

A backend-driven web application to manage student academic records and generate result reports.
The system allows administrators to manage students, subjects, and marks while generating performance reports automatically.

---

## 🚀 Features

* Student management (Add, view, delete students)
* Subject management
* Result entry for each subject
* Automatic grade calculation
* Individual student result report
* Overall performance report for all students
* RESTful API endpoints
* SQLite database integration
* Sample data seeding for testing

---

## 🛠 Tech Stack

Backend:

* Python
* Flask

Database:

* SQLite
* SQL queries

Other Tools:

* Flask-CORS
* Git
* REST API

---

## 📂 Project Structure

student-result-system
│
├── app.py            # Main Flask API server
├── database.py       # Database connection and schema
├── seed.py           # Insert sample data
├── results.db        # SQLite database
├── requirements.txt  # Python dependencies
├── templates         # HTML frontend (optional)
└── README.md

---

## ⚙️ Setup Instructions

### 1. Clone Repository

git clone https://github.com/sreelakshmi1593/student-result-system.git

cd student-result-system

### 2. Create Virtual Environment

python -m venv venv

Activate environment:

Windows:
venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Initialize Database

python database.py

### 5. Seed Sample Data

python seed.py

### 6. Run Application

python app.py

Server will start at:

http://127.0.0.1:5001

---

## 📡 API Endpoints

### Students

GET /api/students
Returns all students

POST /api/students
Add new student

GET /api/students/{id}
Get student by ID

DELETE /api/students/{id}
Delete student

---

### Subjects

GET /api/subjects
Get all subjects

POST /api/subjects
Add subject

---

### Results

POST /api/results
Add marks for a subject

GET /api/results/{student_id}
Get results for a student

---

### Reports

GET /api/report/{student_id}
Generate full report for a student

GET /api/report/all
Generate report summary for all students

---

## 📊 Example Output

Student Report Example:

{
"name": "Priya Sharma",
"roll_number": "CS001",
"percentage": 86.4,
"overall_grade": "A"
}

---

## 💡 Future Improvements

* Student login system
* Admin dashboard
* Search result by roll number
* Result analytics charts
* PDF marksheet download
* React frontend dashboard

---

## 👩‍💻 Author

Sree Lakshmi
Python Developer | Full Stack Developer

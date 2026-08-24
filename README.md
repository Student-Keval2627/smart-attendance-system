<div align="center">

<img src="client/images/logo.png" alt="SmartAttend Logo" width="95" />

# 🎓 SmartAttend

### Smart College Attendance Management System

A clean, responsive and easy-to-use attendance management web application built for teachers using **Flask, SQLite, HTML and CSS**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

---

## 📌 About the Project

**SmartAttend** is a teacher-focused college attendance management system designed to simplify everyday attendance work.

Teachers can create an account, manage their profile, create classes, add students, collect daily attendance and view attendance history. Attendance percentages are calculated automatically from saved attendance records.

The project uses a lightweight architecture and stores data locally with SQLite, making it simple to run and demonstrate without requiring a separate database server.

---

## ✨ Features

- 🔐 Teacher registration and login
- 👨‍🏫 Teacher profile management
- 🏫 Create and manage classes
- 👨‍🎓 Add and manage students
- 🗑️ Delete classes and students with confirmation
- 📅 Select attendance date up to the current date
- ✅ Mark students as Present
- ❌ Unselected students are automatically marked Absent
- 🔄 Reopen and update attendance for the same date
- 📊 Automatic attendance percentage calculation
- 🕒 Date-wise attendance history
- 👁️ View individual student attendance records
- 📱 Responsive, mobile-friendly interface
- 🔒 Passwords stored securely using password hashing

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3 |
| Backend | Python, Flask |
| Database | SQLite |
| Template Engine | Jinja2 |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
smart-attendance-system/
│
├── client/
│   ├── css/                 # Page styling
│   ├── images/              # Logo and images
│   └── pages/               # HTML/Jinja templates
│
├── server/
│   ├── database/
│   │   ├── database.py      # Database connection/setup
│   │   └── schema.sql       # Database schema
│   │
│   ├── models/              # Application models
│   ├── routes/              # Flask route modules
│   ├── services/            # Application services
│   ├── app.py               # Flask application entry point
│   └── config.py            # Configuration
│
├── .gitignore
└── README.md
```

---

## 🗄️ Database

The application uses **SQLite** with the following main tables:

- `teachers`
- `classes`
- `students`
- `attendance`

Attendance percentage is calculated from actual attendance records rather than being entered manually.

> The local SQLite database file is excluded from GitHub through `.gitignore` so personal teacher/student data is not committed to the repository.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Student-Keval2627/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create a virtual environment (recommended)

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Flask

```bash
pip install flask
```

### 4. Create the SQLite database

```bash
cd server
python database/database.py
```

### 5. Run the application

```bash
python app.py
```

### 6. Open in your browser

```text
http://127.0.0.1:5000
```

---

## 🔄 Application Flow

```text
Teacher Login / Registration
          ↓
    Complete Profile
          ↓
         Home
          ↓
    Create / Open Class
          ↓
      Add Students
          ↓
   Collect Attendance
          ↓
  Present / Absent Saved
          ↓
Percentage + History Updated
```

---

## 🎯 Design Goals

The interface is intentionally designed to be:

- Simple and easy for teachers to understand
- Clean and distraction-free
- Responsive on desktop and mobile screens
- Consistent across every page
- Fast to use during daily attendance collection

---

## 🔮 Possible Future Improvements

- Export attendance reports to CSV/PDF
- Search and filter students
- Monthly attendance reports
- Admin dashboard
- Cloud database support
- Deployment for online access
- Student login/view-only portal

---

## 🤝 Contributing

Suggestions and improvements are welcome. You can fork the repository, create a new branch and submit a pull request.

---

## 👨‍💻 Author

**Keval**  
GitHub: [@Student-Keval2627](https://github.com/Student-Keval2627)

---

<div align="center">

### ⭐ If you find this project useful, consider giving the repository a star!

**Built for simpler and smarter attendance management.**

</div>

<div align="center">

<img src="client/images/logo.png" alt="SmartAttend Logo" width="95" />

# 🎓 SmartAttend

### Smart College Attendance Management System

A responsive attendance management web application for teachers, built with **Python Flask, MongoDB Atlas, HTML and CSS** and designed for cloud deployment on **Render**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Render](https://img.shields.io/badge/Render-Cloud-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>

---

## 📌 About

**SmartAttend** is a practical teacher-focused attendance system for managing classes, students and attendance from a single web application.

The application now uses **MongoDB Atlas as a central cloud database**, allowing the same teacher, class, student and attendance data to be available from different devices when the website is deployed online.

Attendance is organized into three fixed college-use categories:

- 📘 **Theory**
- 🧪 **Practical**
- 📝 **Tutorial**

No separate subject setup is required. A teacher opens a class, selects one of the three attendance categories, chooses a date and marks students Present or Absent.

---

## ✨ Current Features

- 🔐 Teacher registration and secure login
- 👨‍🏫 Teacher profile management
- 🏫 Create and manage classes
- 👨‍🎓 Add and manage students
- 🗑️ Delete classes and students with confirmation
- 📅 Attendance date selection with future dates blocked
- 📘 Theory attendance
- 🧪 Practical attendance
- 📝 Tutorial attendance
- ✅ Present checkbox workflow
- ❌ Unselected students automatically marked Absent
- 🔄 Reopen and update the same date + attendance type
- 📊 Automatic overall attendance percentage
- 📈 Separate Theory / Practical / Tutorial percentages
- 🕒 Attendance history by date and attendance type
- 👁️ Individual student attendance history
- ☁️ MongoDB Atlas central data storage
- 📱 Responsive mobile-friendly interface
- 🔒 Password hashing using Werkzeug
- 🚀 Ready for Render deployment

---

## 🏗️ Architecture

```text
Teacher Phone / Laptop
          │
          ▼
   Render Live Website
          │
          ▼
     Flask Backend
          │
          ▼
    MongoDB Atlas
          │
          ├── teachers
          ├── classes
          ├── students
          └── attendance
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3 |
| Backend | Python, Flask |
| Database | MongoDB Atlas |
| Database Driver | PyMongo |
| Templates | Jinja2 |
| Production Server | Gunicorn |
| Hosting | Render |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
smart-attendance-system/
│
├── client/
│   ├── css/                  # Page styling
│   ├── images/               # Logo and images
│   └── pages/                # Jinja HTML templates
│
├── server/
│   ├── database/
│   │   ├── database.py       # MongoDB Atlas connection + indexes
│   │   ├── migrate_sqlite_to_mongo.py
│   │   └── schema.sql        # Legacy SQLite schema
│   │
│   ├── models/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── class_routes.py
│   │   ├── student_routes.py
│   │   └── attendance_routes.py
│   │
│   ├── services/
│   ├── app.py
│   └── config.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗄️ MongoDB Collections

### `teachers`
Stores teacher login and profile data.

### `classes`
Stores classes owned by each teacher.

### `students`
Stores student details linked to a class.

### `attendance`
Stores one record per student for each attendance session.

Example:

```json
{
  "student_id": "ObjectId",
  "class_id": "ObjectId",
  "teacher_id": "ObjectId",
  "attendance_date": "2026-08-27",
  "attendance_type": "Practical",
  "status": "Present"
}
```

A unique MongoDB index prevents duplicate attendance for the same student, class, date and attendance type.

---

## 🔄 Attendance Flow

```text
Teacher Login
     ↓
Dashboard
     ↓
Open Class
     ↓
Collect Attendance
     ↓
Select Category
┌───────────┬────────────┬───────────┐
│  Theory   │ Practical  │ Tutorial  │
└───────────┴────────────┴───────────┘
     ↓
Select Date
     ↓
Mark Present Students
     ↓
Submit
     ↓
MongoDB Atlas
     ↓
Percentage + History Updated
```

---

## 🚀 Local Setup

### 1. Clone

```bash
git clone https://github.com/Student-Keval2627/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env` and add your MongoDB Atlas connection string.

```env
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=smart_attendance
SECRET_KEY=replace-with-a-long-random-secret
FLASK_DEBUG=1
```

> Never commit your real MongoDB password or `MONGO_URI` to GitHub.

### 5. Run

```powershell
cd server
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔁 One-Time SQLite → MongoDB Migration

If you still have the old local file:

```text
server/database/attendance.db
```

install dependencies, configure `.env`, then from the `server` directory run:

```powershell
python -m database.migrate_sqlite_to_mongo
```

The migration transfers teachers, classes, students and attendance into an **empty MongoDB database**.

> Legacy attendance did not contain an attendance category, so migrated legacy records are stored as **Theory** attendance.

---

## ☁️ Render Deployment

Recommended environment variables on Render:

```text
MONGO_URI
MONGO_DB_NAME=smart_attendance
SECRET_KEY
FLASK_DEBUG=0
```

If the Render service root directory is the repository root, use:

```bash
gunicorn --chdir server app:app
```

If the Render root directory is already set to `server`, use:

```bash
gunicorn app:app
```

Build command:

```bash
pip install -r requirements.txt
```

If Render's root directory is `server`, use `pip install -r ../requirements.txt` instead.

---

## 🔐 Security

- Passwords are stored as hashes, not plain text.
- MongoDB credentials are loaded from environment variables.
- `.env` and local `.db` files are ignored by Git.
- Teachers can only access classes and students that belong to their own account.

---

## 🗺️ Next Improvements

- Admin login and central admin dashboard
- Teacher, class and student data management from admin side
- Search and filtering
- Monthly and category-wise reports
- CSV / Excel / PDF export
- Dashboard statistics
- PWA / installable mobile app experience
- Audit logs and stronger production security

---

## 👨‍💻 Author

**Keval**  
GitHub: [@Student-Keval2627](https://github.com/Student-Keval2627)

---

<div align="center">

### ⭐ Smart attendance, central data, practical workflow.

</div>

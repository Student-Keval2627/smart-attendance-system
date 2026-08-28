<div align="center">

<img src="client/icons/icon-512.png" alt="SmartAttend Logo" width="100" />

# SmartAttend

### Smart College Attendance Management System

A modern, cloud-based and installable attendance management system built for **teachers and administrators**.

SmartAttend provides class management, student management, attendance tracking, analytics, centralized administration and Progressive Web App support in one simple platform.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB Atlas" />
  <img src="https://img.shields.io/badge/PWA-Installable-5A0FC8?style=flat-square&logo=pwa&logoColor=white" alt="PWA" />
  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render" />
  <img src="https://img.shields.io/badge/Status-Completed-2EA44F?style=flat-square" alt="Status" />
</p>

**Simple Attendance • Central Management • Mobile Ready**

[Overview](#overview) •
[Screenshots](#screenshots) •
[Features](#features) •
[Architecture](#system-architecture) •
[Setup](#local-setup) •
[Deployment](#render-deployment)

</div>

---

## Overview

**SmartAttend** is a full-stack college attendance management system designed to simplify attendance work for teachers while providing administrators with centralized control over the complete system.

Teachers can:

- Create and manage classes
- Add and manage students
- Record attendance
- View attendance history
- Monitor student attendance percentages

Administrators can:

- Monitor teachers
- View classes
- View students
- Monitor attendance records
- Filter attendance
- View attendance statistics

All application data is stored centrally using **MongoDB Atlas**, allowing the system to work across different devices after deployment.

SmartAttend is also configured as a **Progressive Web App (PWA)**, allowing supported browsers to install it like a desktop or mobile application.

---

## Attendance Categories

SmartAttend uses exactly three attendance categories:

| Category | Purpose |
|---|---|
| 📘 **Theory** | Classroom / lecture attendance |
| 🧪 **Practical** | Laboratory / practical attendance |
| 📝 **Tutorial** | Tutorial / guided-session attendance |

No separate subject configuration is required.

This keeps the attendance workflow simple and fast.

---

# Screenshots

> Screenshots below contain sample development data only. Passwords and database credentials are not displayed.

## Teacher Login

<p align="center">
  <img
    src="docs/screenshots/teacher-login.png"
    alt="SmartAttend Teacher Login"
    width="900"
  />
</p>

<p align="center">
  <strong>Secure teacher authentication with direct administrator access.</strong>
</p>

---

## Teacher Dashboard

<p align="center">
  <img
    src="docs/screenshots/teacher-dashboard.png"
    alt="SmartAttend Teacher Dashboard"
    width="900"
  />
</p>

<p align="center">
  <strong>Manage classes, students and attendance from a simple teacher workspace.</strong>
</p>

---

## Admin Dashboard

<p align="center">
  <img
    src="docs/screenshots/admin-dashboard.png"
    alt="SmartAttend Admin Dashboard"
    width="900"
  />
</p>

<p align="center">
  <strong>Centralized system monitoring and attendance analytics for administrators.</strong>
</p>

---

# Features

## 👨‍🏫 Teacher Module

### Authentication

- Secure teacher registration
- Secure teacher login
- Session-based authentication
- Password hashing using Werkzeug
- Teacher logout
- Teacher profile management

### Class Management

- Create classes
- View teacher-owned classes
- Delete classes
- Class-wise student management

### Student Management

- Add students
- Delete students
- Store student roll number
- Store student information
- View students by class
- Individual student attendance view

### Attendance Management

- Attendance date selection
- Future attendance dates are blocked
- Theory attendance
- Practical attendance
- Tutorial attendance
- Checkbox-based Present marking
- Unchecked students automatically become Absent
- Existing attendance can be reopened
- Same date + attendance type updates existing records
- Duplicate attendance records are prevented

### Attendance Analytics

- Overall attendance percentage
- Theory attendance percentage
- Practical attendance percentage
- Tutorial attendance percentage
- Attendance history
- Attendance grouped by date
- Attendance grouped by type
- Student-specific attendance history

---

## 🛡️ Admin Module

SmartAttend includes a separate administrator system.

### Admin Authentication

- Separate admin login
- Hashed admin password
- Session-based admin authentication
- Admin logout

Admin route:

```text
/admin/login
```

### Admin Dashboard

The dashboard provides:

- Total Teachers
- Total Classes
- Total Students
- Total Attendance Records

It also provides attendance statistics for:

- Theory
- Practical
- Tutorial

### Teacher Management

Administrators can:

- View registered teachers
- Search teachers
- View teacher-related class statistics
- View teacher-related student statistics

### Class Management

Administrators can:

- View all classes
- Search classes
- View assigned teachers
- View student counts

### Student Management

Administrators can:

- View all students
- Search students
- View class information
- View teacher information
- View attendance percentage

### Attendance Management

Attendance can be filtered using:

- Date
- Attendance Type
- Class
- Teacher

The administrator can also view:

- Total attendance records
- Present count
- Absent count
- Attendance percentage

---

# 📱 Progressive Web App

SmartAttend includes complete PWA support.

### PWA Features

- Web App Manifest
- Service Worker
- Install SmartAttend button
- Custom application icon
- Desktop installation
- Mobile installation
- Offline fallback page
- Static asset caching
- Responsive user interface

The application can be installed from supported browsers like a normal app.

### Installation Flow

```text
Open SmartAttend
       ↓
Browser Detects PWA
       ↓
Install SmartAttend
       ↓
Confirm Installation
       ↓
SmartAttend Added to Device
```

> The custom installation button appears only when the browser considers SmartAttend installable.

If SmartAttend is already installed, the install button normally stays hidden.

---

# ☁️ Cloud Architecture

SmartAttend uses a centralized cloud architecture.

```text
┌───────────────────────────────────────────────┐
│               Teacher / Admin                 │
│          Mobile • Tablet • Laptop             │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│               SmartAttend PWA                 │
│                                               │
│          HTML • CSS • JavaScript              │
│                 Jinja2                        │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                Flask Backend                  │
│                                               │
│  Authentication                              │
│  Teacher Management                          │
│  Class Management                            │
│  Student Management                          │
│  Attendance Management                       │
│  Admin Management                            │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                MongoDB Atlas                  │
│                                               │
│  admins                                       │
│  teachers                                     │
│  classes                                      │
│  students                                     │
│  attendance                                   │
└───────────────────────────────────────────────┘
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 |
| Styling | CSS3 |
| Client Logic | JavaScript |
| Templates | Jinja2 |
| Backend | Python |
| Web Framework | Flask |
| Database | MongoDB Atlas |
| Database Driver | PyMongo |
| Authentication | Flask Session |
| Password Security | Werkzeug |
| PWA | Manifest + Service Worker |
| Production Server | Gunicorn |
| Hosting | Render |
| Version Control | Git |
| Repository | GitHub |

---

# Database Design

SmartAttend uses five primary MongoDB collections.

| Collection | Description |
|---|---|
| `admins` | Administrator authentication data |
| `teachers` | Teacher accounts and profiles |
| `classes` | Classes belonging to teachers |
| `students` | Students belonging to classes |
| `attendance` | Student attendance records |

---

## Attendance Uniqueness

Attendance uniqueness is maintained using:

```text
student_id
+
class_id
+
attendance_date
+
attendance_type
```

This prevents duplicate records.

For example:

```text
Student: 101
Date: 2026-08-28
Type: Practical
```

If the teacher opens the same session again, SmartAttend updates the existing record instead of creating another duplicate attendance entry.

---

## Attendance Document Example

```json
{
  "student_id": "ObjectId(...)",
  "class_id": "ObjectId(...)",
  "attendance_date": "2026-08-28",
  "attendance_type": "Practical",
  "status": "Present"
}
```

---

# Teacher Workflow

```text
Teacher Login
      ↓
Teacher Dashboard
      ↓
Create / Open Class
      ↓
Manage Students
      ↓
Collect Attendance
      ↓
Select Date
      ↓
Select Attendance Type
      ↓
┌─────────────┬─────────────┬─────────────┐
│   Theory    │  Practical  │  Tutorial   │
└─────────────┴─────────────┴─────────────┘
      ↓
Mark Present Students
      ↓
Submit Attendance
      ↓
MongoDB Atlas
      ↓
Attendance History Updated
      ↓
Attendance Percentage Updated
```

---

# Admin Workflow

```text
Teacher Login Page
        ↓
Admin Login
        ↓
Admin Dashboard
        ↓
┌──────────┬─────────┬──────────┬────────────┐
│ Teachers │ Classes │ Students │ Attendance │
└──────────┴─────────┴──────────┴────────────┘
        ↓
Search • Filter • Monitor
```

---

# Project Structure

```text
smart-attendance-system/
│
├── client/
│   │
│   ├── css/
│   │   ├── login.css
│   │   ├── admin.css
│   │   ├── pwa.css
│   │   └── ...
│   │
│   ├── icons/
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   │
│   ├── images/
│   │
│   ├── js/
│   │   └── pwa.js
│   │
│   ├── pages/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── home.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_teachers.html
│   │   ├── admin_classes.html
│   │   ├── admin_students.html
│   │   ├── admin_attendance.html
│   │   └── ...
│   │
│   ├── manifest.json
│   ├── offline.html
│   └── service-worker.js
│
├── docs/
│   │
│   └── screenshots/
│       ├── teacher-login.png
│       ├── teacher-dashboard.png
│       └── admin-dashboard.png
│
├── server/
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── class_routes.py
│   │   ├── student_routes.py
│   │   ├── attendance_routes.py
│   │   └── admin_routes.py
│   │
│   ├── create_admin.py
│   └── app.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/Student-Keval2627/smart-attendance-system.git
```

Move into the project:

```bash
cd smart-attendance-system
```

---

## 2. Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

Use `.env.example` as reference.

Example:

```env
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority

MONGO_DB_NAME=smart_attendance

ADMIN_USERNAME=your-admin-username

ADMIN_PASSWORD=your-strong-admin-password

SECRET_KEY=replace-with-a-long-random-secret

FLASK_DEBUG=1
```

> ⚠️ Never commit your real `.env`, MongoDB URI, database password or admin password to GitHub.

---

## 5. Create Admin Account

Move into the server directory:

```powershell
cd server
```

Run:

```powershell
python create_admin.py
```

The script will:

- Create an administrator account when none exists
- Update the administrator password when the account already exists

---

## 6. Run SmartAttend

```powershell
python app.py
```

Teacher application:

```text
http://127.0.0.1:5000/
```

Admin login:

```text
http://127.0.0.1:5000/admin/login
```

---

# Render Deployment

SmartAttend is ready for Render deployment.

## Build Command

```bash
pip install -r requirements.txt
```

## Start Command

```bash
gunicorn --chdir server app:app
```

---

## Render Environment Variables

Configure:

```text
MONGO_URI
```

```text
MONGO_DB_NAME=smart_attendance
```

```text
SECRET_KEY
```

```text
FLASK_DEBUG=0
```

For administrator creation when required:

```text
ADMIN_USERNAME
```

```text
ADMIN_PASSWORD
```

---

# Security

SmartAttend follows practical security controls.

- Teacher passwords are stored as hashes
- Administrator passwords are stored as hashes
- Plain-text passwords are never displayed
- MongoDB credentials use environment variables
- `.env` is excluded from Git
- MongoDB indexes prevent duplicate attendance records
- Teacher-owned classes are validated by backend routes
- Student access follows class ownership
- Future attendance dates are blocked
- Private attendance pages are not cached by the Service Worker
- Service Worker caching is limited primarily to static assets

---

# Project Status

<div align="center">

## ✅ Core Development Completed

</div>

| Module | Status |
|---|:---:|
| Teacher Registration | ✅ |
| Teacher Login | ✅ |
| Teacher Profile | ✅ |
| Class Management | ✅ |
| Student Management | ✅ |
| Theory Attendance | ✅ |
| Practical Attendance | ✅ |
| Tutorial Attendance | ✅ |
| Attendance History | ✅ |
| Attendance Statistics | ✅ |
| Admin Login | ✅ |
| Admin Dashboard | ✅ |
| Admin Teacher Management | ✅ |
| Admin Class Management | ✅ |
| Admin Student Management | ✅ |
| Admin Attendance Management | ✅ |
| MongoDB Atlas Integration | ✅ |
| Responsive Mobile UI | ✅ |
| PWA Support | ✅ |
| PWA App Icons | ✅ |
| Offline Fallback | ✅ |
| Render Deployment | ✅ |
| GitHub Version Control | ✅ |

---

# Future Improvements

Possible future versions of SmartAttend may include:

- Student login portal
- Excel attendance export
- CSV export
- PDF reports
- QR-based attendance
- Attendance shortage alerts
- Student notifications
- Department management
- Semester management
- Multi-college support
- Advanced charts
- Advanced analytics
- Audit logs
- Role-based permissions
- Email notifications

---

# Author

<div align="center">

### Keval Radadiya

Developer of **SmartAttend**

[![GitHub](https://img.shields.io/badge/GitHub-Student--Keval2627-181717?style=for-the-badge&logo=github)](https://github.com/Student-Keval2627)

### Project Repository

[![Repository](https://img.shields.io/badge/Repository-SmartAttend-5B8DEF?style=for-the-badge&logo=github)](https://github.com/Student-Keval2627/smart-attendance-system)

</div>

---

<div align="center">

## Smart Attendance. Central Data. Practical Workflow.

Built with ❤️ using

**Python • Flask • MongoDB Atlas • JavaScript • PWA**

⭐ If you find SmartAttend useful, consider giving the repository a star.

</div>

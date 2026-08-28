<div align="center">

<img src="client/icons/icon-512.png" alt="SmartAttend Logo" width="100" />

# SmartAttend

### Smart College Attendance Management System

A modern, cloud-ready and installable attendance management platform designed for **teachers and administrators**.

Built with **Flask, MongoDB Atlas and Progressive Web App technology** for a simple, responsive and practical college attendance workflow.

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
[Architecture](#architecture) •
[Setup](#local-setup) •
[Deployment](#render-deployment)

</div>

---

## Overview

**SmartAttend** is a full-stack college attendance management system that simplifies attendance handling for teachers while providing administrators with a centralized view of the complete system.

Teachers can create classes, manage students, collect attendance and view attendance statistics.

Administrators can monitor teachers, classes, students and attendance records from a dedicated admin dashboard.

SmartAttend stores all application data in **MongoDB Atlas**, making data centrally available across multiple devices after deployment.

The application is also configured as a **Progressive Web App (PWA)**, allowing supported browsers to install SmartAttend like a desktop or mobile application.

---

## Attendance Categories

SmartAttend intentionally uses exactly three attendance categories:

| Category | Purpose |
|---|---|
| 📘 **Theory** | Classroom / Lecture Attendance |
| 🧪 **Practical** | Laboratory / Practical Attendance |
| 📝 **Tutorial** | Tutorial / Guided Session Attendance |

No separate subject configuration is required.

This keeps the attendance workflow simple and practical.

---

## Screenshots

> Screenshots shown below use sample development data. No passwords or database credentials are displayed.

### Teacher Login

<p align="center">
  <img
    src="docs/screenshots/teacher-login.png"
    alt="SmartAttend Teacher Login"
    width="850"
  />
</p>

---

### Teacher Dashboard

<p align="center">
  <img
    src="docs/screenshots/teacher-dashboard.png"
    alt="SmartAttend Teacher Dashboard"
    width="850"
  />
</p>

---

### Admin Dashboard

<p align="center">
  <img
    src="docs/screenshots/admin-dashboard.png"
    alt="SmartAttend Admin Dashboard"
    width="850"
  />
</p>
---

### Admin Dashboard

<p align="center">
  <img
    src="docs/screenshots/admin-dashboard.jpg"
    alt="SmartAttend Admin Dashboard"
    width="850"
  />
</p>

---

## Features

### 👨‍🏫 Teacher Module

- Secure teacher registration
- Secure teacher login
- Password hashing using Werkzeug
- Teacher profile management
- Create classes
- Delete classes
- Add students
- Delete students
- View class-wise students
- Collect attendance by date
- Future attendance dates are blocked
- Theory attendance
- Practical attendance
- Tutorial attendance
- Checkbox-based Present marking
- Unchecked students automatically marked Absent
- Existing attendance can be updated
- Duplicate attendance records are prevented
- Attendance history grouped by date and type
- Individual student attendance history
- Overall attendance percentage
- Theory attendance percentage
- Practical attendance percentage
- Tutorial attendance percentage

---

### 🛡️ Admin Module

- Separate administrator login
- Central admin dashboard
- Total teacher count
- Total class count
- Total student count
- Total attendance record count
- Theory attendance statistics
- Practical attendance statistics
- Tutorial attendance statistics
- Teacher management
- Class management
- Student management
- Attendance management
- Search functionality
- Attendance filtering

Attendance can be filtered by:

- Date
- Attendance Type
- Class
- Teacher

Admin can also view:

- Present count
- Absent count
- Attendance percentage

---

### 📱 PWA & Mobile Experience

SmartAttend includes Progressive Web App support.

Features include:

- Responsive mobile-friendly interface
- Web App Manifest
- Service Worker
- Installable SmartAttend application
- Custom application icon
- Offline fallback page
- Static asset caching
- Install SmartAttend button
- Desktop installation support
- Mobile installation support

Private attendance pages are not stored for offline viewing.

---

### ☁️ Cloud & Production

- MongoDB Atlas cloud database
- Flask backend
- PyMongo database integration
- Gunicorn production server
- Render deployment support
- Environment variable configuration
- Git version control
- GitHub repository management

---

## Architecture

```text
┌───────────────────────────────────────────┐
│            Teacher / Admin                │
│        Mobile • Tablet • Laptop           │
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│             SmartAttend UI                │
│         HTML • CSS • JavaScript           │
│                Jinja2                     │
│             PWA Support                   │
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│             Flask Backend                 │
│                                           │
│  Authentication                           │
│  Classes                                  │
│  Students                                 │
│  Attendance                               │
│  Administration                           │
└─────────────────────┬─────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────┐
│             MongoDB Atlas                 │
│                                           │
│  admins                                   │
│  teachers                                 │
│  classes                                  │
│  students                                 │
│  attendance                               │
└───────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Template Engine | Jinja2 |
| Backend | Python, Flask |
| Database | MongoDB Atlas |
| Database Driver | PyMongo |
| Authentication | Flask Session |
| Password Security | Werkzeug |
| PWA | Manifest + Service Worker |
| Production Server | Gunicorn |
| Hosting | Render |
| Version Control | Git |
| Repository Hosting | GitHub |

---

## Database Design

SmartAttend uses five primary MongoDB collections.

### `admins`

Stores administrator login information.

### `teachers`

Stores teacher account and profile information.

### `classes`

Stores classes created by teachers.

### `students`

Stores students belonging to classes.

### `attendance`

Stores attendance records for students.

---

### Attendance Unique Record

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

This prevents duplicate attendance records.

If a teacher opens the same:

```text
Date + Attendance Type
```

again, the existing attendance is updated instead of creating duplicate records.

---

### Example Attendance Document

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

## Teacher Workflow

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

## Admin Workflow

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

Admin login route:

```text
/admin/login
```

---

## Project Structure

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
│   └── screenshots/
│       ├── teacher-login.jpg
│       ├── teacher-dashboard.jpg
│       └── admin-dashboard.jpg
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

Create a private:

```text
.env
```

file.

Example:

```env
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority

MONGO_DB_NAME=smart_attendance

ADMIN_USERNAME=your-admin-username

ADMIN_PASSWORD=your-strong-admin-password

SECRET_KEY=replace-with-a-long-random-secret

FLASK_DEBUG=1
```

> ⚠️ Never upload your real `.env`, MongoDB password, admin password or database URI to GitHub.

---

## 5. Create Admin Account

Move to server folder:

```powershell
cd server
```

Run:

```powershell
python create_admin.py
```

The script will:

- Create admin if it does not exist
- Update admin password if the account already exists

---

## 6. Start SmartAttend

```powershell
python app.py
```

Teacher Login:

```text
http://127.0.0.1:5000/
```

Admin Login:

```text
http://127.0.0.1:5000/admin/login
```

---

# Render Deployment

SmartAttend is ready for deployment using Render.

## Build Command

```bash
pip install -r requirements.txt
```

---

## Start Command

```bash
gunicorn --chdir server app:app
```

---

## Environment Variables

Configure the following variables in Render:

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

Admin configuration when required:

```text
ADMIN_USERNAME
ADMIN_PASSWORD
```

---

# PWA Installation

SmartAttend can be installed like a normal application.

### Installation Flow

```text
Open SmartAttend Website
        ↓
Browser Checks PWA
        ↓
Install SmartAttend Button
        ↓
Install
        ↓
SmartAttend Added to Device
```

On supported browsers:

1. Open SmartAttend.
2. Wait until the application becomes installable.
3. Click **Install SmartAttend**.
4. Confirm installation.
5. Open SmartAttend from your desktop or mobile home screen.

> The custom install button appears only when the browser fires the PWA installation event.

If the application is already installed, the install button will normally remain hidden.

---

# Security

SmartAttend follows practical security practices.

- Teacher passwords are hashed.
- Admin passwords are hashed.
- Passwords are never displayed in the UI.
- MongoDB credentials use environment variables.
- `.env` is excluded from Git.
- MongoDB indexes prevent duplicate records.
- Teacher-owned classes are validated by backend routes.
- Student access is restricted through class ownership.
- Future attendance dates are blocked.
- Private application pages are not cached by the Service Worker.
- Static assets are safely cached for PWA functionality.

---

# Project Status

## ✅ Core Development Completed

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
| Attendance Percentage | ✅ |
| Admin Login | ✅ |
| Admin Dashboard | ✅ |
| Admin Teacher Management | ✅ |
| Admin Class Management | ✅ |
| Admin Student Management | ✅ |
| Admin Attendance Management | ✅ |
| MongoDB Atlas | ✅ |
| Responsive UI | ✅ |
| PWA Support | ✅ |
| Render Deployment | ✅ |

---

# Future Improvements

Possible future versions may include:

- Student login portal
- Excel report export
- CSV report export
- PDF attendance reports
- QR-based attendance
- Student attendance shortage alerts
- Notifications
- Department management
- Semester management
- Multi-college support
- Advanced dashboard charts
- Audit logs
- Role-based permissions
- Attendance analytics

---

# Author

<div align="center">

### Keval Radadiya

Developer of **SmartAttend**

[![GitHub](https://img.shields.io/badge/GitHub-Student--Keval2627-181717?style=for-the-badge&logo=github)](https://github.com/Student-Keval2627)

### Repository

[![Repository](https://img.shields.io/badge/Repository-SmartAttend-5B8DEF?style=for-the-badge&logo=github)](https://github.com/Student-Keval2627/smart-attendance-system)

</div>

---

<div align="center">

## Smart Attendance. Central Data. Practical Workflow.

Built with ❤️ using **Python • Flask • MongoDB Atlas**

⭐ If you find SmartAttend useful, consider giving the repository a star.

</div>

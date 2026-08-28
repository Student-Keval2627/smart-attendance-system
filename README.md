<div align="center">

<img src="client/icons/icon-192.png" alt="SmartAttend Logo" width="110" />

# 🎓 SmartAttend

### Smart College Attendance Management System

A complete, responsive and installable attendance management system built with **Flask + MongoDB Atlas**, designed for teachers and administrators and deployed as a cloud-ready web app.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Render](https://img.shields.io/badge/Render-Cloud-46E3B7?style=for-the-badge&logo=render&logoColor=black)
![PWA](https://img.shields.io/badge/PWA-Installable-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

**Simple • Fast • Smart Attendance**

</div>

---

## 📌 Overview

**SmartAttend** is a college attendance management system that allows teachers to manage classes, students and attendance while giving administrators a central dashboard to monitor the complete system.

The application stores data in **MongoDB Atlas**, so the same information is available across devices when deployed online. It is also configured as a **Progressive Web App (PWA)**, allowing supported browsers to install SmartAttend like an app on desktop or mobile.

Attendance is intentionally simple and uses exactly three fixed categories:

- 📘 **Theory**
- 🧪 **Practical**
- 📝 **Tutorial**

No separate subject configuration is required.

---

## ✨ Features

### 👨‍🏫 Teacher Module

- Secure teacher registration and login
- Password hashing with Werkzeug
- Teacher profile management
- Create and delete classes
- Add and delete students
- View class-wise student lists
- Collect attendance by date
- Future attendance dates are blocked
- Theory / Practical / Tutorial attendance
- Checkbox-based Present marking
- Unchecked students are automatically marked Absent
- Same date + category updates existing attendance instead of creating duplicates
- Attendance history grouped by date and category
- Individual student attendance details
- Overall attendance percentage
- Separate Theory / Practical / Tutorial percentages

### 🛡️ Admin Module

- Separate admin login
- Central admin dashboard
- Total teacher count
- Total class count
- Total student count
- Total attendance record count
- Theory / Practical / Tutorial statistics
- Teacher management view
- Class management view
- Student management view
- Attendance management view
- Search and filtering
- Attendance filtering by date, category, class and teacher
- Present / Absent summary and attendance percentage

### 📱 PWA & Mobile Experience

- Responsive mobile-friendly UI
- Web App Manifest
- Service Worker
- Installable SmartAttend app
- Custom app icons
- Offline fallback page
- Static asset caching
- Private attendance pages are not cached for offline viewing

### ☁️ Cloud & Production

- MongoDB Atlas cloud database
- Flask backend
- Gunicorn production server
- Render deployment support
- Environment-variable based configuration
- Git / GitHub version control

---

## 🏗️ System Architecture

```text
┌──────────────────────────────┐
│     Teacher / Admin Device   │
│   Mobile • Tablet • Laptop   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      SmartAttend Web/PWA     │
│      HTML • CSS • Jinja      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Flask Backend         │
│ Auth • Classes • Students    │
│ Attendance • Admin           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        MongoDB Atlas         │
│ admins • teachers • classes  │
│ students • attendance        │
└──────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Templates | Jinja2 |
| Backend | Python, Flask |
| Database | MongoDB Atlas |
| Database Driver | PyMongo |
| Authentication | Flask Session + Werkzeug Password Hashing |
| PWA | Manifest + Service Worker |
| Production Server | Gunicorn |
| Hosting | Render |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
smart-attendance-system/
│
├── client/
│   ├── css/                    # Application styles
│   ├── icons/                  # PWA app icons
│   ├── images/                 # Project images
│   ├── js/
│   │   └── pwa.js              # PWA registration + install button
│   ├── pages/                  # Jinja HTML templates
│   │   ├── login.html
│   │   ├── home.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   └── ...
│   ├── manifest.json           # PWA manifest
│   ├── offline.html            # Offline fallback page
│   └── service-worker.js       # PWA service worker
│
├── server/
│   ├── database/
│   │   └── database.py         # MongoDB connection + indexes
│   ├── routes/
│   │   ├── auth.py             # Teacher authentication
│   │   ├── home.py             # Teacher dashboard/home
│   │   ├── class_routes.py     # Class management
│   │   ├── student_routes.py   # Student management
│   │   ├── attendance_routes.py# Attendance management
│   │   └── admin_routes.py     # Admin module
│   ├── create_admin.py         # Create/update admin account
│   └── app.py                  # Flask application entry point
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🗄️ MongoDB Collections

SmartAttend uses five main collections:

| Collection | Purpose |
|---|---|
| `admins` | Admin login credentials |
| `teachers` | Teacher account and profile data |
| `classes` | Classes linked to teachers |
| `students` | Students linked to classes |
| `attendance` | Student attendance records |

Attendance uniqueness is enforced for the same student, class, date and attendance type, preventing duplicate attendance sessions.

Example attendance document:

```json
{
  "student_id": "ObjectId(...) ",
  "class_id": "ObjectId(...) ",
  "attendance_date": "2026-08-28",
  "attendance_type": "Practical",
  "status": "Present"
}
```

---

## 🔄 Teacher Attendance Flow

```text
Teacher Login
     ↓
Teacher Home
     ↓
Open Class
     ↓
Select Attendance
     ↓
Choose Date
     ↓
Choose Category
     ↓
Theory / Practical / Tutorial
     ↓
Mark Present Students
     ↓
Submit Attendance
     ↓
MongoDB Atlas
     ↓
History + Percentages Updated
```

---

## 🛡️ Admin Flow

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

## 🚀 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Student-Keval2627/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create `.env`

Create a private `.env` file using `.env.example` as the template:

```env
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=smart_attendance
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-strong-admin-password
SECRET_KEY=replace-with-a-long-random-secret
FLASK_DEBUG=1
```

> ⚠️ Never commit your real MongoDB URI, database password, admin password or `.env` file to GitHub.

### 5. Create the admin account

From the `server` folder:

```powershell
cd server
python create_admin.py
```

The script creates the admin account if it does not exist, or updates the admin password if it already exists.

### 6. Run SmartAttend

```powershell
python app.py
```

Open the teacher application:

```text
http://127.0.0.1:5000/
```

Open admin login directly:

```text
http://127.0.0.1:5000/admin/login
```

---

## ☁️ Render Deployment

Recommended Render configuration:

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn --chdir server app:app
```

### Environment Variables

```text
MONGO_URI=<MongoDB Atlas connection string>
MONGO_DB_NAME=smart_attendance
SECRET_KEY=<long random secret>
FLASK_DEBUG=0
```

For admin creation, configure `ADMIN_USERNAME` and `ADMIN_PASSWORD` when running `create_admin.py` in an environment where the same MongoDB database is accessible.

---

## 📲 Install as an App

SmartAttend includes PWA support.

On a supported browser:

1. Open the deployed SmartAttend website.
2. Wait for the browser to confirm the site is installable.
3. Click **Install SmartAttend** when the install button appears, or use the browser's install option.
4. Launch SmartAttend from the desktop/home screen like a normal app.

> The custom install button is only shown when the browser fires the PWA install prompt. It may not appear when the app is already installed or the browser does not currently consider the site installable.

---

## 🔐 Security Practices

- Teacher and admin passwords are stored as hashes.
- MongoDB credentials are read from environment variables.
- `.env` is ignored by Git.
- Database indexes help prevent duplicate data.
- Teacher-owned class/student access is validated by backend routes.
- Future attendance dates are blocked.
- Service worker caching is limited to static assets; private attendance pages use network access.

---

## ✅ Project Status

**SmartAttend core development is complete.**

Completed modules:

- ✅ Teacher Authentication
- ✅ Teacher Profile
- ✅ Class Management
- ✅ Student Management
- ✅ Theory / Practical / Tutorial Attendance
- ✅ Attendance History & Statistics
- ✅ Admin Login & Dashboard
- ✅ Admin Data Management
- ✅ MongoDB Atlas Integration
- ✅ Responsive Mobile UI
- ✅ PWA Installation
- ✅ Render Deployment Support

---

## 🗺️ Possible Future Enhancements

- Student login portal
- Excel / CSV / PDF reports
- QR-based attendance
- Notifications
- Department / semester management
- Multi-college support
- Advanced charts and analytics
- Attendance shortage alerts
- Audit logs

---

## 👨‍💻 Author

**Keval**  
GitHub: [@Student-Keval2627](https://github.com/Student-Keval2627)

Repository: [smart-attendance-system](https://github.com/Student-Keval2627/smart-attendance-system)

---

<div align="center">

### ⭐ Smart attendance. Central management. Simple workflow.

If you find this project useful, consider giving the repository a ⭐.

</div>

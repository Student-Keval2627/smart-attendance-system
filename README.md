


<div align="center">

<img src="client/icons/icon-512.png" alt="SmartAttend Logo" width="96" />

SmartAttend
Smart College Attendance Management System
A cloud-ready attendance management platform for colleges, built for teachers and administrators with a clean workflow, centralized data, and installable PWA support.

<p> <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" /> <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB Atlas" /> <img src="https://img.shields.io/badge/PWA-Installable-5A0FC8?style=flat-square&logo=pwa&logoColor=white" alt="PWA" /> <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render" /> <img src="https://img.shields.io/badge/Status-Completed-2EA44F?style=flat-square" alt="Project Status" /> </p>

Simple attendance. Central management. Mobile-ready.

Overview • Screenshots • Features • Architecture • Setup • Deployment

</div>

Overview
SmartAttend is a full-stack attendance management system designed for college use. Teachers can create classes, manage students, collect attendance, and review attendance history. Administrators get a central dashboard to monitor teachers, classes, students, and attendance records across the system.

The application stores data in MongoDB Atlas, so the same data is available across devices after deployment. It also includes Progressive Web App (PWA) support, allowing supported browsers to install SmartAttend like a desktop or mobile app.

Attendance is intentionally organized into exactly three categories:

Category	Use
Theory	Classroom / lecture attendance
Practical	Laboratory / practical attendance
Tutorial	Tutorial / guided-session attendance
No separate subject setup is required, keeping the workflow fast and simple.

Screenshots
Screenshots below use sample development data. No passwords or database credentials are shown.

<table> <tr> <td width="50%" align="center"> <img src="docs/screenshots/teacher-login.jpg" alt="SmartAttend Teacher Login" /> <br /> <strong>Teacher Login</strong> </td> <td width="50%" align="center"> <img src="docs/screenshots/teacher-dashboard.jpg" alt="SmartAttend Teacher Dashboard" /> <br /> <strong>Teacher Dashboard</strong> </td> </tr> </table>

<p align="center"> <img src="docs/screenshots/admin-dashboard.jpg" alt="SmartAttend Admin Dashboard" width="900" /> <br /> <strong>Admin Dashboard & Attendance Analytics</strong> </p>

Features
Teacher workspace
Secure teacher registration and login

Werkzeug password hashing

Teacher profile management

Create and delete classes

Add and delete students

Class-wise student management

Collect attendance by date

Future attendance dates are blocked

Fixed attendance types: Theory, Practical, Tutorial

Checkbox-based Present marking

Unchecked students are saved as Absent

Reopening the same date + type updates existing records

Attendance history grouped by date and type

Individual student attendance history

Overall attendance percentage

Separate Theory / Practical / Tutorial percentages

Admin workspace
Separate administrator login

Central system dashboard

Teacher, class, student, and attendance totals

Theory / Practical / Tutorial analytics

Teacher management view

Class management view

Student management view

Attendance management view

Search and filtering

Filter attendance by:

date

attendance type

class

teacher

Present / Absent summaries and attendance percentage

PWA and mobile experience
Responsive mobile-friendly interface

Web App Manifest

Service Worker

Installable SmartAttend app

Custom application icons

Offline fallback page

Static asset caching

Private attendance pages are not cached for offline viewing

Cloud and production
MongoDB Atlas centralized database

Flask backend

PyMongo database integration

Gunicorn production server

Render deployment support

Environment-variable configuration

Git and GitHub version control

Architecture
┌───────────────────────────────────────────────┐
│              Teacher / Admin                 │
│          Mobile • Tablet • Laptop            │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│               SmartAttend UI                  │
│          HTML • CSS • JS • Jinja2            │
│               PWA support                     │
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                Flask Backend                  │
│ Auth • Classes • Students • Attendance • Admin│
└──────────────────────┬────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────┐
│                MongoDB Atlas                  │
│ admins • teachers • classes • students        │
│ attendance                                    │
└───────────────────────────────────────────────┘
Tech Stack
Layer	Technology
Frontend	HTML5, CSS3, JavaScript
Templates	Jinja2
Backend	Python, Flask
Database	MongoDB Atlas
Database Driver	PyMongo
Authentication	Flask Session + Werkzeug
PWA	Manifest + Service Worker
Production Server	Gunicorn
Hosting	Render
Version Control	Git + GitHub
Database Design
SmartAttend uses five primary collections:

Collection	Purpose
admins	Administrator credentials
teachers	Teacher account and profile data
classes	Classes linked to teachers
students	Students linked to classes
attendance	Attendance records for each student/session
Attendance uniqueness is enforced for:

student_id + class_id + attendance_date + attendance_type
This prevents duplicate attendance records when a teacher reopens an existing attendance session.

Example attendance document:

{
  "student_id": "ObjectId(...)",
  "class_id": "ObjectId(...)",
  "attendance_date": "2026-08-28",
  "attendance_type": "Practical",
  "status": "Present"
}
Core Workflow
Teacher flow
Teacher Login
    ↓
Teacher Dashboard
    ↓
Open Class
    ↓
Manage Students
    ↓
Collect Attendance
    ↓
Select Date + Type
    ↓
Mark Present Students
    ↓
Submit
    ↓
MongoDB Atlas
    ↓
History + Percentages Updated
Admin flow
Teacher Login Page
    ↓
Admin Login
    ↓
Admin Dashboard
    ↓
Teachers • Classes • Students • Attendance
    ↓
Search • Filter • Monitor
Direct admin route:

/admin/login
Project Structure
smart-attendance-system/
│
├── client/
│   ├── css/                     # Application styles
│   ├── icons/                   # PWA icons
│   ├── images/                  # Project images
│   ├── js/
│   │   └── pwa.js               # Service worker + install prompt
│   ├── pages/                   # Jinja templates
│   ├── manifest.json            # PWA manifest
│   ├── offline.html             # Offline fallback
│   └── service-worker.js        # Service worker
│
├── docs/
│   └── screenshots/             # README screenshots
│
├── server/
│   ├── database/
│   │   └── database.py          # MongoDB connection + indexes
│   ├── routes/
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── class_routes.py
│   │   ├── student_routes.py
│   │   ├── attendance_routes.py
│   │   └── admin_routes.py
│   ├── create_admin.py
│   └── app.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
Local Setup
1. Clone the repository
git clone https://github.com/Student-Keval2627/smart-attendance-system.git
cd smart-attendance-system
2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install -r requirements.txt
4. Configure environment variables
Create a private .env file from .env.example:

MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=smart_attendance
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-strong-admin-password
SECRET_KEY=replace-with-a-long-random-secret
FLASK_DEBUG=1
Never commit a real MongoDB URI, database password, admin password, or .env file.

5. Create or update the admin account
cd server
python create_admin.py
6. Run SmartAttend
python app.py
Teacher application:

http://127.0.0.1:5000/
Admin login:

http://127.0.0.1:5000/admin/login
Render Deployment
Recommended Render configuration:

Build command
pip install -r requirements.txt
Start command
gunicorn --chdir server app:app
Environment variables
MONGO_URI=<MongoDB Atlas connection string>
MONGO_DB_NAME=smart_attendance
SECRET_KEY=<long random secret>
FLASK_DEBUG=0
If admin creation is required in the deployment environment, also configure:

ADMIN_USERNAME
ADMIN_PASSWORD
PWA Installation
On a supported browser:

Open the deployed SmartAttend website.

Wait for the browser to confirm that the site is installable.

Click Install SmartAttend when the custom install button appears, or use the browser's install option.

Launch SmartAttend from the desktop or home screen.

The custom button only appears when the browser fires the PWA install prompt. It may stay hidden when SmartAttend is already installed or when the browser does not currently consider the site installable.

Security
SmartAttend follows practical security controls for a college project / lightweight production deployment:

Passwords are stored as hashes, not plain text.

Database credentials are loaded from environment variables.

.env is excluded from Git.

MongoDB indexes help prevent duplicate records.

Teacher-owned class and student access is validated in backend routes.

Future attendance dates are blocked.

Service Worker caching is limited to static assets.

Private attendance pages use network access instead of offline page caching.

Project Status
Core development is complete.

Module	Status
Teacher Authentication	✅ Complete
Teacher Profile	✅ Complete
Class Management	✅ Complete
Student Management	✅ Complete
Theory / Practical / Tutorial Attendance	✅ Complete
Attendance History & Statistics	✅ Complete
Admin Login & Dashboard	✅ Complete
Admin Data Management	✅ Complete
MongoDB Atlas Integration	✅ Complete
Responsive UI	✅ Complete
PWA Installation	✅ Complete
Render Deployment Support	✅ Complete
Future Improvements
Student login portal

Excel / CSV / PDF reports

QR-based attendance

Attendance shortage alerts

Notifications

Department / semester management

Multi-college support

Advanced analytics and charts

Audit logs

Author
Keval Radadiya

GitHub: @Student-Keval2627

Repository: smart-attendance-system

<div align="center">

Smart attendance. Central data. Practical workflow.
If this project is useful to you, consider giving the repository a ⭐.

</div>


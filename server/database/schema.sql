-- ==================================================
-- SMART COLLEGE ATTENDANCE SYSTEM DATABASE
-- ==================================================


-- ==================================================
-- 1. TEACHERS
-- ==================================================

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,

    name TEXT,
    mobile TEXT,
    age INTEGER,
    qualification TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==================================================
-- 2. CLASSES
-- ==================================================

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    teacher_id INTEGER NOT NULL,

    class_name TEXT NOT NULL,
    batch TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (teacher_id)
        REFERENCES teachers(id)
        ON DELETE CASCADE
);


-- ==================================================
-- 3. STUDENTS
-- ==================================================

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    class_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    mobile TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (class_id)
        REFERENCES classes(id)
        ON DELETE CASCADE,

    UNIQUE (
        class_id,
        roll_no
    )
);


-- ==================================================
-- 4. ATTENDANCE
-- ==================================================

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,

    attendance_date DATE NOT NULL,

    status TEXT NOT NULL
        CHECK (
            status IN ('Present', 'Absent')
        ),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    FOREIGN KEY (class_id)
        REFERENCES classes(id)
        ON DELETE CASCADE,

    FOREIGN KEY (teacher_id)
        REFERENCES teachers(id)
        ON DELETE CASCADE,

    UNIQUE (
        student_id,
        class_id,
        attendance_date
    )
);


-- ==================================================
-- 5. INDEXES
-- ==================================================

CREATE INDEX IF NOT EXISTS idx_classes_teacher
ON classes(teacher_id);


CREATE INDEX IF NOT EXISTS idx_students_class
ON students(class_id);


CREATE INDEX IF NOT EXISTS idx_attendance_student
ON attendance(student_id);


CREATE INDEX IF NOT EXISTS idx_attendance_class
ON attendance(class_id);


CREATE INDEX IF NOT EXISTS idx_attendance_teacher
ON attendance(teacher_id);


CREATE INDEX IF NOT EXISTS idx_attendance_date
ON attendance(attendance_date);
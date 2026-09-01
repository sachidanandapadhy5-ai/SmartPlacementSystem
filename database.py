import sqlite3


def create_database():
    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dsa_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lectures_completed INTEGER DEFAULT 0,
            problems_solved INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT,
            technology TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            progress INTEGER DEFAULT 0,
            status TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    cursor.execute("""
        INSERT INTO subjects (name, progress, status)
        SELECT 'DBMS', 20, 'In Progress'
        WHERE NOT EXISTS (
            SELECT 1 FROM subjects WHERE name = 'DBMS'
        )
    """)

    cursor.execute("""
        INSERT INTO subjects (name, progress, status)
        SELECT 'Operating Systems', 15, 'In Progress'
        WHERE NOT EXISTS (
            SELECT 1 FROM subjects WHERE name = 'Operating Systems'
        )
    """)

    cursor.execute("""
        INSERT INTO subjects (name, progress, status)
        SELECT 'Computer Networks', 0, 'Not Started'
        WHERE NOT EXISTS (
            SELECT 1 FROM subjects WHERE name = 'Computer Networks'
        )
    """)

    cursor.execute("""
        INSERT INTO projects (name, description, status, technology)
        SELECT
            'Smart Placement Preparation System',
            'A web application for tracking placement preparation.',
            'In Development',
            'Python, Flask, SQLite'
        WHERE NOT EXISTS (
            SELECT 1 FROM projects
            WHERE name = 'Smart Placement Preparation System'
        )
    """)

    cursor.execute("""
        INSERT INTO projects (name, description, status, technology)
        SELECT
            'AI Resume Analyzer',
            'Resume analysis and ATS-style scoring application.',
            'Completed',
            'Python, Streamlit, PDF Processing'
        WHERE NOT EXISTS (
            SELECT 1 FROM projects
            WHERE name = 'AI Resume Analyzer'
        )
    """)

    cursor.execute("""
        INSERT INTO projects (name, description, status, technology)
        SELECT
            'Page Replacement Simulator',
            'Operating System project implementing page replacement algorithms.',
            'Completed',
            'C'
        WHERE NOT EXISTS (
            SELECT 1 FROM projects
            WHERE name = 'Page Replacement Simulator'
        )
    """)

    cursor.execute("""
        INSERT INTO dsa_progress (lectures_completed, problems_solved)
        SELECT 40, 0
        WHERE NOT EXISTS (SELECT 1 FROM dsa_progress)
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
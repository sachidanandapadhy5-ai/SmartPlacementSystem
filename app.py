from flask import Flask, render_template, request, redirect, url_for
from database import create_database
import sqlite3

app = Flask(__name__)
create_database()


@app.route("/")
def home():
    progress = get_dsa_progress()
    total_tasks, completed_tasks, pending_tasks = get_task_summary()

    return render_template(
        "index.html",
        lectures_completed=progress[0],
        problems_solved=progress[1],
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )

def get_dsa_progress():
    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT lectures_completed, problems_solved FROM dsa_progress"
    )

    progress = cursor.fetchone()

    connection.close()

    return progress

def get_projects():
    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, description, status, technology
        FROM projects
    """)

    projects = cursor.fetchall()

    connection.close()

    return projects

def get_subjects():
    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, progress, status
        FROM subjects
    """)

    subjects = cursor.fetchall()

    connection.close()

    return subjects

def get_tasks():

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, description, status
        FROM tasks
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks

def get_task_summary():

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Completed'
    """)
    completed_tasks = cursor.fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    connection.close()

    return total_tasks, completed_tasks, pending_tasks

@app.route("/dsa")
def dsa():
    progress = get_dsa_progress()

    progress_percentage = (progress[0] / 100) * 100

    return render_template(
        "dsa.html",
        lectures_completed=progress[0],
        problems_solved=progress[1],
        progress_percentage=progress_percentage
    )

@app.route("/update-dsa", methods=["POST"])
def update_dsa():

    lectures = request.form["lectures"]
    problems = request.form["problems"]

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE dsa_progress
        SET lectures_completed = ?, problems_solved = ?
        WHERE id = 1
    """, (lectures, problems))

    connection.commit()
    connection.close()

    return redirect(url_for("dsa"))

@app.route("/subjects")
def subjects():
    subjects = get_subjects()

    return render_template(
        "subjects.html",
        subjects=subjects
    )

@app.route("/update-subject/<int:subject_id>", methods=["POST"])
def update_subject(subject_id):

    progress = request.form["progress"]

    try:
        progress = int(progress)
    except ValueError:
        return "Invalid progress value", 400

    if progress < 0 or progress > 100:
        return "Progress must be between 0 and 100", 400

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE subjects
        SET progress = ?
        WHERE id = ?
    """, (progress, subject_id))

    connection.commit()
    connection.close()

    return redirect(url_for("subjects"))

@app.route("/projects")
def projects():
    projects = get_projects()

    return render_template(
        "projects.html",
        projects=projects
    )

@app.route("/add-project", methods=["POST"])
def add_project():

    name = request.form["name"]
    description = request.form["description"]
    status = request.form["status"]
    technology = request.form["technology"]

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO projects (name, description, status, technology)
        VALUES (?, ?, ?, ?)
    """, (name, description, status, technology))

    connection.commit()
    connection.close()

    return redirect(url_for("projects"))

@app.route("/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("projects"))

@app.route("/tasks")
def tasks():

    tasks = get_tasks()
    total_tasks, completed_tasks, pending_tasks = get_task_summary()

    return render_template(
        "tasks.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )

@app.route("/clear-completed-tasks", methods=["POST"])
def clear_completed_tasks():

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE status = 'Completed'
    """)

    connection.commit()
    connection.close()

    return redirect(url_for("tasks"))

@app.route("/add-task", methods=["POST"])
def add_task():

    title = request.form["title"]
    description = request.form["description"]

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description)
        VALUES (?, ?)
    """, (title, description))

    connection.commit()
    connection.close()

    return redirect(url_for("tasks"))

@app.route("/complete-task/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("tasks"))

@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("tasks"))

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):

    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)


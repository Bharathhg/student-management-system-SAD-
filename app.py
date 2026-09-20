from flask import Flask, render_template, request
import sqlite3
import os
from create_database import DB_PATH, DB_DIR, init_db

app = Flask(__name__)

# Ensure DB exists on startup
if not os.path.exists(DB_PATH):
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    usn = request.form["usn"]
    dept = request.form["dept"]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students(name, usn, dept) VALUES (?, ?, ?)",
        (name, usn, dept)
    )
    conn.commit()
    conn.close()
    
    return f"""
    <div style="font-family: Arial; width: 420px; margin: 50px auto; padding: 25px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2 style="color: #28a745;">Student Registered Successfully</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>USN:</b> {usn}</p>
        <p><b>Department:</b> {dept}</p>
        <br>
        <a href="/" style="color: #007bff; text-decoration: none; font-weight: bold;">← Register Another Student</a>
        &nbsp;|&nbsp;
        <a href="/students" style="color: #28a745; text-decoration: none; font-weight: bold;">View All Students →</a>
    </div>
    """

@app.route("/students")
def list_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, usn, dept FROM students ORDER BY id DESC")
    students = cursor.fetchall()
    conn.close()
    
    rows = "".join([f"<tr><td style='padding:8px;border:1px solid #ddd;'>{s[0]}</td><td style='padding:8px;border:1px solid #ddd;'>{s[1]}</td><td style='padding:8px;border:1px solid #ddd;'>{s[2]}</td><td style='padding:8px;border:1px solid #ddd;'>{s[3]}</td></tr>" for s in students])
    
    return f"""
    <div style="font-family: Arial; width: 600px; margin: 40px auto; padding: 25px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2>Registered Students List</h2>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px; border: 1px solid #ddd;">ID</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Name</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">USN</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Dept</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else "<tr><td colspan='4' style='text-align:center;padding:15px;'>No students registered yet.</td></tr>"}
            </tbody>
        </table>
        <br>
        <a href="/" style="color: #007bff; text-decoration: none; font-weight: bold;">← Back to Registration</a>
    </div>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


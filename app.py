from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Ensure DB exists on startup
if not os.path.exists("students.db"):
    from create_database import init_db
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    usn = request.form["usn"]
    dept = request.form["dept"]
    
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students(name, usn, dept) VALUES (?, ?, ?)",
        (name, usn, dept)
    )
    conn.commit()
    conn.close()
    
    return f"""
    <div style="font-family: Arial; width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2 style="color: #28a745;">Student Registered Successfully</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>USN:</b> {usn}</p>
        <p><b>Department:</b> {dept}</p>
        <br>
        <a href="/" style="color: #007bff; text-decoration: none; font-weight: bold;">← Register Another Student</a>
    </div>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

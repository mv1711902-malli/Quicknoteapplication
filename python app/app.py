
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "notes.db"


# Create database and table
def create_table():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Connect to database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Get all saved notes
@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_db_connection()

    notes = conn.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(note) for note in notes])


# Save a new note
@app.route("/api/notes", methods=["POST"])
def save_note():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Please enter a note."}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )

    note_id = cursor.lastrowid
    conn.commit()

    note = conn.execute(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(note)), 201


# Delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Note not found."}), 404

    return jsonify({"message": "Note deleted successfully."})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)

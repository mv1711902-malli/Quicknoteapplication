
const noteInput = document.getElementById("noteInput");
const notesList = document.getElementById("notesList");


// Display all saved notes
async function loadNotes() {

    try {
        const response = await fetch("/api/notes");

        if (!response.ok) {
            throw new Error("Unable to load notes");
        }

        const notes = await response.json();

        notesList.innerHTML = "";

        if (notes.length === 0) {
            notesList.textContent = "No notes saved yet.";
            return;
        }

        notes.forEach(note => {

            const div = document.createElement("div");
            div.className = "note";

            const paragraph = document.createElement("p");
            paragraph.textContent = note.content;

            const date = document.createElement("small");
            date.textContent = "Created: " + note.created_at;

            const button = document.createElement("button");
            button.textContent = "Delete";
            button.className = "delete-btn";

            button.addEventListener("click", () => {
                deleteNote(note.id);
            });

            div.append(paragraph, date, button);
            notesList.appendChild(div);

        });

    } catch (error) {
        notesList.textContent = "Error loading notes.";
    }
}


// Save a new note
async function saveNote() {

    const content = noteInput.value.trim();

    if (content === "") {
        alert("Please enter a note!");
        return;
    }

    try {
        const response = await fetch("/api/notes", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                content: content
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Unable to save note");
        }

        noteInput.value = "";

        alert("Note saved successfully!");

        loadNotes();

    } catch (error) {
        alert(error.message);
    }
}


// Delete a note
async function deleteNote(id) {

    if (!confirm("Are you sure you want to delete this note?")) {
        return;
    }

    try {
        const response = await fetch(`/api/notes/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Unable to delete note");
        }

        alert("Note deleted successfully!");

        loadNotes();

    } catch (error) {
        alert(error.message);
    }
}


// Load notes when the page opens
document.addEventListener("DOMContentLoaded", loadNotes);

# ToDoApp

---

**Introduction to the To-Do List App:**

The To-Do List App is a simple yet powerful tool designed to help you manage your tasks effectively. Whether you're organizing your daily activities, planning projects, or prioritizing your goals, this app provides a convenient way to keep track of your tasks in one place.

**Features:**
- **Add Tasks:** Quickly add new tasks with titles, priorities, and due dates.
- **Update Tasks:** Modify existing tasks by updating their titles, priorities, or due dates.
- **Delete Tasks:** Remove tasks from your list that are no longer needed.
- **Sort Tasks:** Arrange your tasks by title, priority, or due date for better organization.

**How to Use the App:**

**Graphical User Interface (GUI):**
1. Launch the To-Do List App by running the provided Python script (`todo_app.py`).
2. Use the input fields to add a new task by entering a title, selecting a priority, and choosing a due date.
3. Click the "Add Task" button to add the task to your list.
4. To update a task, select it from the list and click the "Update Task" button. You can then modify the title, priority, or due date as needed.
5. To delete a task, select it from the list and click the "Delete Task" button.
6. Use the "Sort by Title", "Sort by Priority", or "Sort by Due Date" buttons to arrange your tasks accordingly.

**Command-Line Interface (CLI):**
- Use command-line arguments to perform specific actions:
  - `--add`: Add a new task by providing the title, priority, and due date.
  - `--list`: Display a list of all tasks.
  - `--delete <index>`: Delete a task by its index.
  - `--update <index>`: Update a task by its index.
  - `--sort <criterion>`: Sort tasks by title, priority, or due date.

**Example CLI Usage:**
- `python todo_app.py --add`: Add a new task interactively.
- `python todo_app.py --list`: List all tasks.
- `python todo_app.py --delete 2`: Delete the task at index 2.
- `python todo_app.py --update 1`: Update the task at index 1.
- `python todo_app.py --sort priority`: Sort tasks by priority.

**Note:** Make sure to have Python and PyQt5 installed to run the graphical user interface.

---

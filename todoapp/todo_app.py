import sys
import argparse
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QInputDialog, QLabel, QComboBox, QDateEdit, QListWidgetItem, QCheckBox
from PyQt5.QtCore import QDate, Qt

class Task:
    def __init__(self, title, description, priority, due_date):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False  # Default status is incomplete

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 400, 300)
        
        self.tasks = []
        
        self.layout = QVBoxLayout()
        
        self.title_label = QLabel("Title:")
        self.input_field = QLineEdit()
        self.priority_label = QLabel("Priority:")
        self.priority_field = QComboBox()
        self.priority_field.addItems(["1", "2", "3"])
        self.due_date_label = QLabel("Due Date:")
        self.due_date_field = QDateEdit()
        self.due_date_field.setDisplayFormat("dd/MM/yyyy")
        self.add_button = QPushButton("Add Task")
        self.update_button = QPushButton("Update Task")
        self.delete_button = QPushButton("Delete Task")
        self.sort_title_button = QPushButton("Sort by Title")
        self.sort_priority_button = QPushButton("Sort by Priority")
        self.sort_due_date_button = QPushButton("Sort by Due Date")
        self.task_list = QListWidget()
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.priority_label)
        self.layout.addWidget(self.priority_field)
        self.layout.addWidget(self.due_date_label)
        self.layout.addWidget(self.due_date_field)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.sort_title_button)
        self.layout.addWidget(self.sort_priority_button)
        self.layout.addWidget(self.sort_due_date_button)
        self.layout.addWidget(self.task_list)
        
        self.add_button.clicked.connect(self.add_task)
        self.update_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.sort_title_button.clicked.connect(self.sort_by_title)
        self.sort_priority_button.clicked.connect(self.sort_by_priority)
        self.sort_due_date_button.clicked.connect(self.sort_by_due_date)
        
        self.task_list.itemChanged.connect(self.update_task_status)
        
        self.setLayout(self.layout)
        
        self.load_tasks()  # Load tasks when the app starts
    
    def add_task(self):
        title = self.input_field.text()
        priority = self.priority_field.currentText()
        due_date = self.due_date_field.date().toString("yyyy-MM-dd")
        
        if title:
            task = Task(title, "", priority, due_date)
            self.tasks.append(task)
            self.update_task_list()
            self.input_field.clear()
            self.save_tasks()  # Save tasks after adding
        
    def update_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item is not None:
            index = self.task_list.currentRow()
            current_task = self.tasks[index]
            new_title, ok = QInputDialog.getText(self, "Update Task", "Enter new title:", QLineEdit.Normal, current_task.title)
            if ok:
                new_priority, ok = QInputDialog.getItem(self, "Update Task", "Select new priority:", ["1", "2", "3"], int(current_task.priority) - 1)
                if ok:
                    new_due_date, ok = QInputDialog.getText(self, "Update Task", "Enter new due date (dd/MM/yyyy):", QLineEdit.Normal, self.due_date_field.date().toString("dd/MM/yyyy"))
                    if ok:
                        year_suffix = new_due_date[-2:]  # Get the last two digits of the input year
                        new_due_date_str = QDate.fromString(new_due_date, "dd/MM/yyyy").toString("yyyy-MM-dd")
                        self.tasks[index] = Task(new_title, current_task.description, new_priority, new_due_date_str)
                        self.update_task_list()
                        self.save_tasks()  # Save tasks after updating
        
    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item is not None:
            index = self.task_list.currentRow()
            del self.tasks[index]
            self.task_list.takeItem(index)
            self.save_tasks()  # Save tasks after deleting

    def sort_by_title(self):
        self.tasks.sort(key=lambda x: x.title)
        self.update_task_list()
    
    def sort_by_priority(self):
        self.tasks.sort(key=lambda x: x.priority)
        self.update_task_list()
    
    def sort_by_due_date(self):
        self.tasks.sort(key=lambda x: x.due_date)
        self.update_task_list()
    
    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            item = QListWidgetItem(f"{task.title} - Priority: {task.priority}, Due Date: {task.due_date}")
            if task.completed:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.task_list.addItem(item)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

    def update_task_status(self, item):
        index = self.task_list.row(item)
        task = self.tasks[index]
        task.completed = item.checkState() == Qt.Checked
        self.save_tasks()  # Save tasks after updating status

    def save_tasks(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.tasks, file)
    
    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                self.tasks = pickle.load(file)
                self.update_task_list()
        except FileNotFoundError:
            # File not found, so there are no tasks to load
            pass

def run_cli():
    parser = argparse.ArgumentParser(description="To-Do List CLI")
    parser.add_argument("--add", help="Add a task", action="store_true")
    parser.add_argument("--list", help="List all tasks", action="store_true")
    parser.add_argument("--delete", help="Delete a task by index")
    parser.add_argument("--update", help="Update a task by index")
    parser.add_argument("--sort", help="Sort tasks by criterion (title, priority, due_date)")
    parser.add_argument("--complete", help="Mark a task as complete by index")
    parser.add_argument("--incomplete", help="Mark a task as incomplete by index")
    args = parser.parse_args()

    if args.add:
        title = input("Enter title: ")
        priority = input("Enter priority (1, 2, or 3): ")
        due_date = input("Enter due date (yyyy/MM/dd): ")
        task = Task(title, "", priority, due_date)
        app = QApplication(sys.argv)
        window = ToDoApp()
        window.tasks.append(task)
        window.save_tasks()
        print("Task added successfully.")
        sys.exit()

    if args.list:
        try:
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                print("Tasks:")
                for i, task in enumerate(tasks):
                    status = "Completed" if task.completed else "Incomplete"
                    print(f"{i + 1}. {task.title} - Priority: {task.priority}, Due Date: {task.due_date} ({status})")
        except FileNotFoundError:
            print("No tasks found.")
        sys.exit()

    if args.delete:
        try:
            index = int(args.delete) - 1
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                if 0 <= index < len(tasks):
                    del tasks[index]
                    with open("tasks.pkl", "wb") as file:
                        pickle.dump(tasks, file)
                    print("Task deleted successfully.")
                else:
                    print("Invalid task index.")
        except (FileNotFoundError, ValueError):
            print("Error: Unable to delete task.")
        sys.exit()

    if args.update:
        try:
            index = int(args.update) - 1
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                if 0 <= index < len(tasks):
                    title = input("Enter new title: ")
                    priority = input("Enter new priority (1, 2, or 3): ")
                    due_date = input("Enter new due date (yyyy/MM/dd): ")
                    tasks[index] = Task(title, "", priority, due_date)
                    with open("tasks.pkl", "wb") as file:
                        pickle.dump(tasks, file)
                    print("Task updated successfully.")
                else:
                    print("Invalid task index.")
        except (FileNotFoundError, ValueError):
            print("Error: Unable to update task.")
        sys.exit()

    if args.sort:
        try:
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                if args.sort == "title":
                    tasks.sort(key=lambda x: x.title)
                elif args.sort == "priority":
                    tasks.sort(key=lambda x: x.priority)
                elif args.sort == "due_date":
                    tasks.sort(key=lambda x: x.due_date)
                else:
                    print("Invalid sorting criterion.")
                    sys.exit()
                with open("tasks.pkl", "wb") as file:
                    pickle.dump(tasks, file)
                print("Tasks sorted successfully.")
        except (FileNotFoundError, ValueError):
            print("Error: Unable to sort tasks.")
        sys.exit()

    if args.complete:
        try:
            index = int(args.complete) - 1
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                if 0 <= index < len(tasks):
                    tasks[index].completed = True
                    with open("tasks.pkl", "wb") as file:
                        pickle.dump(tasks, file)
                    print("Task marked as complete successfully.")
                else:
                    print("Invalid task index.")
        except (FileNotFoundError, ValueError):
            print("Error: Unable to mark task as complete.")
        sys.exit()

    if args.incomplete:
        try:
            index = int(args.incomplete) - 1
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
                if 0 <= index < len(tasks):
                    tasks[index].completed = False
                    with open("tasks.pkl", "wb") as file:
                        pickle.dump(tasks, file)
                    print("Task marked as incomplete successfully.")
                else:
                    print("Invalid task index.")
        except (FileNotFoundError, ValueError):
            print("Error: Unable to mark task as incomplete.")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        app = QApplication(sys.argv)
        window = ToDoApp()
        window.show()
        sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QInputDialog, QLabel, QComboBox, QDateEdit, QListWidgetItem
from PyQt5.QtCore import QDate, QLocale

class Task:
    def __init__(self, title, description, priority, due_date):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date

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
        
        self.setLayout(self.layout)
    
    def add_task(self):
        title = self.input_field.text()
        priority = self.priority_field.currentText()
        due_date = self.due_date_field.date().toString("yyyy-MM-dd")
        
        if title:
            task = Task(title, "", priority, due_date)
            self.tasks.append(task)
            self.update_task_list()
            self.input_field.clear()

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

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item is not None:
            index = self.task_list.currentRow()
            del self.tasks[index]
            self.task_list.takeItem(index)

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
            self.task_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())

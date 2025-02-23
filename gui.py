import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from student import Student

class UniversityGUI:
    def __init__(self, university):
        self.university = university
        self.root = tk.Tk()
        self.root.title("Система управління університетом")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Створення фрейму для дерева
        tree_frame = tk.Frame(self.root, bg='#f0f0f0')
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Створення дерева
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Додавання скроллбару до дерева
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree["columns"] = ("Type",)
        self.tree.column("#0", width=300)
        self.tree.column("Type", width=100)
        self.tree.heading("#0", text="Елемент")
        self.tree.heading("Type", text="Тип")

        self.populate_tree(self.university, "")

        # Створення правої панелі
        right_panel = tk.Frame(self.root, bg='#f0f0f0')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Створення панелі керування
        control_panel = tk.Frame(right_panel, bg='#f0f0f0')
        control_panel.pack(fill=tk.X, pady=10)

        buttons = [
            ("Список студентів групи", self.list_students),
            ("Додати студента", self.add_student),
            ("Видалити студента", self.remove_student),
            ("Інформація про куратора", self.get_curator_info)
        ]

        for text, command in buttons:
            tk.Button(control_panel, text=text, command=command, bg='#4CAF50', fg='white', 
                      activebackground='#45a049', activeforeground='white', bd=0, padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        # Створення нередагованої інформаційної панелі
        self.info_panel = tk.Text(right_panel, wrap=tk.WORD, width=50, bg='white', fg='black', font=('Arial', 10), state='disabled')
        self.info_panel.pack(fill=tk.BOTH, expand=True, pady=10)

    def populate_tree(self, node, parent_id):
        node_id = self.tree.insert(parent_id, "end", text=node.name, values=(node.node_type,))
        for child in node.children:
            self.populate_tree(child, node_id)

    def list_students(self):
        group = self.get_selected_group()
        if group:
            students_info = f"Студенти групи {group.name}:\n"
            for student in group.students:
                students_info += f"{student.first_name} {student.last_name}, "
                students_info += f"Номер залікової книжки: {student.id_code}\n"
            self.update_info(students_info)

    def add_student(self):
        group = self.get_selected_group()
        if not group:
            return

        # Запитуємо дані нового студента
        first_name = simpledialog.askstring("Додати студента", "Введіть ім'я студента:")
        last_name = simpledialog.askstring("Додати студента", "Введіть прізвище студента:")
        id_code = simpledialog.askstring("Додати студента", "Введіть номер залікової книжки (6 цифр):")

        # Перевіряємо коректність введених даних
        if not all([first_name, last_name, id_code]) or not id_code.isdigit() or len(id_code) != 6:
            messagebox.showerror("Помилка", "Неправильно введені дані студента.")
            return

        # Створюємо нового студента і додаємо його до групи
        new_student = Student(first_name, last_name, id_code)
        group.add_student(new_student)
        self.update_info(f"Студент {new_student} доданий до групи {group.name}")
        self.refresh_tree()

    def remove_student(self):
        group = self.get_selected_group()
        if not group:
            return
        if not group.students:
            messagebox.showinfo("Інформація", f"У групі {group.name} немає студентів.")
            return

        # Створюємо список студентів для вибору
        student_list = [f"{student.first_name} {student.last_name}" for student in group.students]
        student_to_remove = simpledialog.askstring(
            "Видалити студента",
            f"Виберіть студента для видалення з групи {group.name}:",
            initialvalue=student_list[0] if student_list else None
        )

        if student_to_remove:
            for student in group.students:
                if f"{student.first_name} {student.last_name}" == student_to_remove:
                    group.remove_student(student)
                    self.update_info(f"Студент {student} видалений з групи {group.name}")
                    self.refresh_tree()
                    return

    def get_curator_info(self):
        department = self.get_selected_department()
        if department:
            # Якщо вибрана кафедра
            curator = department.find_curator()
            if curator:
                self.display_curator_info(curator, f"кафедри {department.name}")
            else:
                self.update_info(f"Інформація про куратора кафедри {department.name} не знайдена.")
        else:
            # Якщо кафедра не вибрана, запитуємо студента
            student_name = simpledialog.askstring("Інформація про куратора", "Введіть ім'я та прізвище студента:")
            if student_name:
                student, group = self.find_student(student_name)
                if student:
                    department = group.parent
                    curator = department.find_curator()
                    if curator:
                        self.display_curator_info(curator, f"студента {student.first_name} {student.last_name}")
                    else:
                        self.update_info(f"Інформація про куратора студента {student_name} не знайдена.")
                else:
                    self.update_info(f"Студент '{student_name}' не знайдений.")

    def display_curator_info(self, curator, entity):
        curator_info = f"Куратор {entity}:\n"
        curator_info += f"Ім'я: {curator['name']}\n"
        curator_info += f"Телефон: {curator['phone']}\n"
        curator_info += f"Email: {curator['email']}"
        self.update_info(curator_info)

    def get_selected_group(self):
        selected_item = self.tree.focus()
        if selected_item:
            item = self.tree.item(selected_item)
            if item['values'][0] == 'група':
                return self.university.find_node(item['text'], 'група')
            
        group_name = simpledialog.askstring("Вибір групи", "Введіть назву групи:")
        if group_name:
            group = self.university.find_node(group_name, 'група')
            if group:
                return group
            else:
                messagebox.showerror("Помилка", f"Група '{group_name}' не знайдена.")
        return None
    
    def get_selected_department(self):
        selected_item = self.tree.focus()
        if selected_item:
            item = self.tree.item(selected_item)
            if item['values'][0] == 'кафедра':
                return self.university.find_node(item['text'], 'кафедра')
        return None

    def find_student(self, student_name):
        for faculty in self.university.children:
            for department in faculty.children:
                for group in department.children:
                    for student in group.students:
                        if f"{student.first_name} {student.last_name}".lower() == student_name.lower():
                            return student, group
        return None, None

    def update_info(self, info):
        self.info_panel.config(state='normal')
        self.info_panel.delete(1.0, tk.END)
        self.info_panel.insert(tk.END, info)
        self.info_panel.config(state='disabled')

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_tree(self.university, "")
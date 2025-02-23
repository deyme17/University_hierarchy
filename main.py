from node import Node
from gui import UniversityGUI

def create_university_structure():
    university = Node("Київський авіаційний інститут", 'Університет')

    faculties = [
        ("Факультет комп'ютерних наук та технологій", [
            ("Кафедра прикладної математики", ["ШІ-218", "ПМ-251"]),
            ("Кафедра інженерії програмного забезпечення", ["ІПЗ-466"]),
            ("Кафедра комп'ютерних інформаційних технологій", ["СІТ-199"])
        ]),
        ("Факультет аеронавігації, електроніки та телекомунікацій", [
            ("Кафедра авіаційних комп'ютерно-інтегрованих комплексів", ["АК-147"]),
            ("Кафедра електроніки, робототехніки і технологій моніторингу та інтернету речей", ["ЕР-188"])
        ]),
        ("Аерокосмічний факультет", [
            ("Кафедра авіаційних двигунів", ["АД-323"]),
            ("Кафедра прикладної механіки та інженерії матеріалів", ["ММ-256"])
        ])
    ]

    for faculty_name, departments in faculties:
        faculty = Node(faculty_name, 'факультет', university)
        university.add_child(faculty)
        
        for dept_name, groups in departments:
            department = Node(dept_name, 'кафедра', faculty)
            faculty.add_child(department)
            
            for group_name in groups:
                group = Node(group_name, 'група', department)
                department.add_child(group)

    # Додаємо кураторів
    curators = {
        "Кафедра прикладної математики": {"name": "Приставка П.О.", "phone": "+380991234567", "email": "prystavka_po@kai.ua"},
        "Кафедра інженерії програмного забезпечення": {"name": "Гріненко О.О.", "phone": "+3802130987", "email": "hrinenkoo@kai.ua"},
        "Кафедра комп'ютерних інформаційних технологій": {"name": "Савченко А.О.", "phone": "+3809871287", "email": "savchenko_alina@kai.ua"},
        "Кафедра авіаційних комп'ютерно-інтегрованих комплексів": {"name": "Синєглазов В.М.", "phone": "+3809993461", "email": "synie2viktor@kai.ua"},
        "Кафедра електроніки, робототехніки і технологій моніторингу та інтернету речей": {"name": "Морозова І.В.", "phone": "+3801209563", "email": "irynamoro70v4@kai.ua"},
        "Кафедра авіаційних двигунів": {"name": "Терещенко Ю.М.", "phone": "+3802309262", "email": "toreshch3n40@kai.ua"},
        "Кафедра прикладної механіки та інженерії матеріалів": {"name": "Мікосянчик О.О.", "phone": "+3803268812", "email": "miko99@kai.ua"}
    }

    for faculty in university.children:
        for department in faculty.children:
            if department.name in curators:
                department.curator = curators[department.name]

    return university

if __name__ == "__main__":
    university = create_university_structure()
    app = UniversityGUI(university)
class Student:
    def __init__(self, first_name, last_name, id_code):
        self.first_name = first_name
        self.last_name = last_name
        self.id_code = id_code
    
    def __repr__(self):
        return f'{self.first_name} {self.last_name}, (ЗК: {self.id_code})'
class Node:
    def __init__(self, name, node_type='Університет', parent=None):
        self.name = name
        self.children = []
        self.node_type = node_type
        self.students = []
        self.curator = None
        self.parent = parent

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def add_student(self, student):
        if self.node_type == 'група':
            self.students.append(student)

    def remove_student(self, student):
        if self.node_type == 'група':
            self.students.remove(student)

    def find_curator(self):
        if self.node_type == 'кафедра' and self.curator:
            return self.curator
        return None
    
    def find_node(self, name, node_type=None):
        if self.name == name and (node_type is None or self.node_type == node_type):
            return self
        for child in self.children:
            result = child.find_node(name, node_type)
            if result:
                return result
        return None

    def __repr__(self):
        return f"{self.name} ({self.node_type})"
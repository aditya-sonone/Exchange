class Field:
    def __init__(self, field_type, name):
        self.field_type = field_type
        self.name = name

    def __repr__(self):
        return f"Field(type={self.field_type}, name={self.name})"


class StructDef:
    def __init__(self, name):
        self.name = name
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def __repr__(self):
        return f"StructDef(name={self.name}, fields={self.fields})"
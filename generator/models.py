class Field:
    def __init__(self, field_type, name):
        self.field_type = field_type
        self.name = name

    def __repr__(self):
        return f"Field(type={self.field_type}, name={self.name})"


class StructDef:

    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"

    def __init__(self, name, packet_id=None, direction="REQUEST"):
        self.name = name
        self.packet_id = packet_id
        self.direction = direction
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def __repr__(self):
        return (
            f"StructDef("
            f"name={self.name}, "
            f"packet_id={self.packet_id}, "
            f"fields={self.fields}"
            f")"
        )
    
class EnumDef:

    def __init__(self, name):
        self.name = name
        self.values = []

    def add_value(self, value):
        self.values.append(value)

    def __repr__(self):
        return (
            f"EnumDef(name={self.name}, "
            f"values={self.values})"
        )
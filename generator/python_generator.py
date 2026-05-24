import struct


class PythonGenerator:

    def __init__(self):

        self.type_map = {
            "uint8": "B",
            "uint16": "H",
            "uint32": "I",
            "uint64": "Q",
        }

        self.default_values = {
            "uint8": "0",
            "uint16": "0",
            "uint32": "0",
            "uint64": "0",
        }

        self.enum_names = set()

    # ---------------- ENUM ----------------

    def generate_enum(self, enum_def):

        lines = []

        lines.append("from enum import IntEnum")
        lines.append("")
        lines.append(f"class {enum_def.name}(IntEnum):")

        for index, value in enumerate(enum_def.values):
            lines.append(f"    {value} = {index}")

        lines.append("")

        return "\n".join(lines)

    # ---------------- STRUCT ----------------

    def generate_struct(self, struct):

        code = []

        code.append("import struct")
        code.append("")

        code.append(f"class {struct.name}:")
        code.append(f"    PACKET_ID = {struct.packet_id}")
        code.append("")

        # ---------------- INIT ----------------

        code.append("    def __init__(self):")

        for f in struct.fields:

            if f.field_type == "string":
                code.append(f'        self.{f.name} = ""')
            else:
                code.append(f"        self.{f.name} = 0")

        code.append("")

        # ---------------- SERIALIZE ----------------

        code.append("    def serialize(self):")
        code.append("        parts = []")

        for f in struct.fields:
            code.append("        " + self.emit_serialize_field(f))

        code.append("")
        code.append("        payload = b''.join(parts)")
        code.append("")

        code.append(
            "        header = struct.pack('<HI', self.PACKET_ID, len(payload))"
        )

        code.append("")

        code.append("        return header + payload")
        code.append("")

        # ---------------- DESERIALIZE ----------------

        code.append("    @staticmethod")
        code.append("    def deserialize(payload: bytes):")

        fmt = self.build_struct_format(struct.fields)

        names = [f.name for f in struct.fields]

        code.append(f"        values = struct.unpack('{fmt}', payload)")
        code.append("")

        code.append(f"        obj = {struct.name}()")
        code.append("")

        for i, name in enumerate(names):
            code.append(f"        obj.{name} = values[{i}]")

        code.append("")
        code.append("        return obj")

        return "\n".join(code)

    # ---------------- SERIALIZE FIELD ----------------

    def emit_serialize_field(self, f):

        fmt = self.type_map.get(f.field_type)

        # Primitive types
        if fmt:
            return f"parts.append(struct.pack('<{fmt}', self.{f.name}))"

        # Enum types
        elif f.field_type in self.enum_names:
            return f"parts.append(struct.pack('<I', int(self.{f.name})))"

        # Strings
        elif f.field_type == "string":

            return (
                f"encoded = self.{f.name}.encode('utf-8')\n"
                f"parts.append(struct.pack('<I', len(encoded)))\n"
                f"parts.append(encoded)"
            )

        else:
            raise Exception(f"Unsupported type: {f.field_type}")

    # ---------------- STRUCT FORMAT ----------------

    def build_struct_format(self, fields):

        fmt = "<"

        for f in fields:

            if f.field_type in self.type_map:
                fmt += self.type_map[f.field_type]

            elif f.field_type in self.enum_names:
                fmt += "I"

            elif f.field_type == "string":
                raise Exception(
                    "Variable-length strings require manual deserialization"
                )

            else:
                raise Exception(
                    f"Unsupported type: {f.field_type}"
                )

        return fmt
    
    def generate_packet_dispatcher(self):
        lines = []

        lines.append(
            "from .packet_registry import PACKET_MAP"
        )

        lines.append("")
        lines.append("")

        lines.append("class PacketDispatcher:")
        lines.append("")

        lines.append("    @staticmethod")
        lines.append("    def dispatch(packet_id, payload):")
        lines.append("")

        lines.append(
            "        packet_cls = PACKET_MAP.get(packet_id)"
        )

        lines.append("")

        lines.append("        if not packet_cls:")
        lines.append(
            "            raise Exception(f'Unknown packet id: {packet_id}')"
        )

        lines.append("")

        lines.append(
            "        return packet_cls.deserialize(payload)"
        )

        return "\n".join(lines)
    
    def generate_packet_registry(self, structs):
        INFRASTRUCTURE_TYPES = {
            "PacketHeader"
        }

        lines = []

        for struct in structs:

            if struct.name in INFRASTRUCTURE_TYPES:
                continue

            lines.append(
                f"from .{struct.name.lower()} import {struct.name}"
            )

        lines.append("")
        lines.append("")

        lines.append("PACKET_MAP = {")
        lines.append("")

        for struct in structs:

            if struct.name in INFRASTRUCTURE_TYPES:
                continue

            lines.append(
                f"    {struct.name}.PACKET_ID: {struct.name},"
            )

        lines.append("")
        lines.append("}")

        return "\n".join(lines)
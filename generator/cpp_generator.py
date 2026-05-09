TYPE_MAP = {
    "uint64": "uint64_t",
    "uint32": "uint32_t",
    "int": "int",
    "double": "double",
    "bool": "bool",
    "string": "std::string"
}


class CppGenerator:

    def cpp_type(self, schema_type):

        return TYPE_MAP.get(schema_type, schema_type)

    def getter_name(self, field_name, field_type):

        capitalized = field_name[0].upper() + field_name[1:]

        if field_type == "bool":
            return f"is{capitalized}"

        return f"get{capitalized}"

    def setter_name(self, field_name):

        capitalized = field_name[0].upper() + field_name[1:]

        return f"set{capitalized}"

    def generate_struct(self, struct_def):

        lines = []

        lines.append("#pragma once")
        lines.append("")

        lines.append("#include <cstdint>")
        lines.append("#include <string>")
        lines.append("")

        lines.append(f"class {struct_def.name}")
        lines.append("{")

        lines.append("private:")

        for field in struct_def.fields:

            cpp_type = self.cpp_type(field.field_type)

            lines.append(
                f"    {cpp_type} {field.name} {{}};"
            )

        lines.append("")
        lines.append("public:")
        lines.append("")

        for field in struct_def.fields:

            cpp_type = self.cpp_type(field.field_type)

            getter_name = self.getter_name(
                field.name,
                field.field_type
            )

            setter_name = self.setter_name(
                field.name
            )

            lines.append(
                f"    {cpp_type} {getter_name}() const"
            )

            lines.append("    {")

            lines.append(
                f"        return {field.name};"
            )

            lines.append("    }")

            lines.append("")

            lines.append(
                f"    void {setter_name}({cpp_type} value)"
            )

            lines.append("    {")

            lines.append(
                f"        {field.name} = value;"
            )

            lines.append("    }")

            lines.append("")

        lines.append("};")

        return "\n".join(lines)
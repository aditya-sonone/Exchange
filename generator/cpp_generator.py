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
    
    def generate_constructor(self, struct_def):

        params = []

        assignments = []

        for field in struct_def.fields:

            cpp_type = self.cpp_type(field.field_type)

            params.append(
                f"{cpp_type} {field.name}"
            )

            assignments.append(
                f"        this->{field.name} = {field.name};"
            )

        lines = []

        lines.append(
            f"    {struct_def.name}("
        )

        for i, param in enumerate(params):

            comma = ","

            if i == len(params) - 1:
                comma = ""

            lines.append(
                f"        {param}{comma}"
            )

        lines.append("    )")
        lines.append("    {")

        lines.extend(assignments)

        lines.append("    }")
        lines.append("")

        return lines

    def generate_struct(self, struct_def):

        lines = []

        lines.append("#pragma once")
        lines.append("")

        lines.append("#include <cstdint>")
        lines.append("#include <string>")
        lines.append("#include <sstream>")
        lines.append("#include <ostream>")
        lines.append("#include <istream>")
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
        constructor_lines = self.generate_constructor(
            struct_def
        )
        lines.extend(constructor_lines)

        to_string_lines = self.generate_to_string(
            struct_def
        )
        lines.extend(to_string_lines)

        serialize_lines = self.generate_serialize(
            struct_def
        )

        lines.extend(serialize_lines)

        deserialize_lines = self.generate_deserialize(
            struct_def
        )

        lines.extend(deserialize_lines)

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
    
    def generate_to_string(self, struct_def):
        lines = []

        lines.append("    std::string toString() const")
        lines.append("    {")

        lines.append("        std::stringstream ss;")

        lines.append(
            f'        ss << "{struct_def.name}{{";'
        )

        for i, field in enumerate(struct_def.fields):

            if i > 0:
                lines.append(
                    '        ss << ", ";'
                )

            lines.append(
                f'        ss << "{field.name}=" << {field.name};'
            )

        lines.append('        ss << "}";')

        lines.append("")

        lines.append("        return ss.str();")

        lines.append("    }")
        lines.append("")

        return lines
    
    def generate_serialize(self, struct_def):
        lines = []

        lines.append(
            "    void serialize(std::ostream& out) const"
        )

        lines.append("    {")

        for field in struct_def.fields:

            if self.is_string_type(field.field_type):

                lines.append(
                    f"        uint32_t {field.name}Size = {field.name}.size();"
                )

                lines.append("")

                lines.append(
                    "        out.write("
                )

                lines.append(
                    f"            reinterpret_cast<const char*>(&{field.name}Size),"
                )

                lines.append(
                    f"            sizeof({field.name}Size)"
                )

                lines.append("        );")

                lines.append("")

                lines.append(
                    f"        out.write({field.name}.data(), {field.name}Size);"
                )

                lines.append("")

            else:

                lines.append(
                    "        out.write("
                )

                lines.append(
                    f"            reinterpret_cast<const char*>(&{field.name}),"
                )

                lines.append(
                    f"            sizeof({field.name})"
                )

                lines.append("        );")

                lines.append("")

        lines.append("    }")
        lines.append("")

        return lines
    
    def generate_deserialize(self, struct_def):
        lines = []

        lines.append(
            "    void deserialize(std::istream& in)"
        )

        lines.append("    {")

        for field in struct_def.fields:

            if self.is_string_type(field.field_type):

                lines.append(
                    f"        uint32_t {field.name}Size;"
                )

                lines.append("")

                lines.append(
                    "        in.read("
                )

                lines.append(
                    f"            reinterpret_cast<char*>(&{field.name}Size),"
                )

                lines.append(
                    f"            sizeof({field.name}Size)"
                )

                lines.append("        );")

                lines.append("")

                lines.append(
                    f"        {field.name}.resize({field.name}Size);"
                )

                lines.append("")

                lines.append(
                    f"        in.read(&{field.name}[0], {field.name}Size);"
                )

                lines.append("")

            else:

                lines.append(
                    "        in.read("
                )

                lines.append(
                    f"            reinterpret_cast<char*>(&{field.name}),"
                )

                lines.append(
                    f"            sizeof({field.name})"
                )

                lines.append("        );")

                lines.append("")

        lines.append("    }")
        lines.append("")

        return lines
    
    def is_string_type(self, field_type):
        return field_type == "string"
TYPE_MAP = {

    "uint8": "uint8_t",
    "uint16": "uint16_t",
    "uint32": "uint32_t",
    "uint64": "uint64_t",

    "int8": "int8_t",
    "int16": "int16_t",
    "int32": "int32_t",
    "int64": "int64_t",

    "float": "float",
    "double": "double",
    "string": "std::string"
}


class CppGenerator:

    def __init__(self):
        self.struct_names = set()
        self.enum_names = set()

    def cpp_type(self, schema_type):
        if self.is_vector_type(schema_type):
            inner = self.get_vector_inner_type(
                schema_type
            )
            cpp_inner = self.cpp_type(inner)
            return f"std::vector<{cpp_inner}>"
        return TYPE_MAP.get(
            schema_type,
            schema_type
        )

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
        lines.append("#include <vector>")
        if struct_def.packet_id is not None:
            lines.append(
                '#include "packetheader.hpp"'
            )
        # Custom type includes
        included_types = set()

        for field in struct_def.fields:
            field_type = field.field_type
            if self.is_vector_type(field_type):
                field_type = self.get_vector_inner_type(
                    field_type
                )
            if not self.is_builtin_type(field_type):
                if field_type not in included_types:
                    include_file = (
                        field_type.lower() + ".hpp"
                    )
                    lines.append(
                        f'#include "{include_file}"'
                    )
                    included_types.add(field_type)

        lines.append("")
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
        if struct_def.packet_id is not None:

            lines.append("")

            lines.append(
                f"    static constexpr uint16_t "
                f"PACKET_ID = {struct_def.packet_id};"
            )
        lines.append("")
        default_constructor_lines = (
            self.generate_default_constructor(
                struct_def
            )
        )

        lines.extend(default_constructor_lines)
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
        binary_size_lines = self.generate_binary_size(
            struct_def
        )

        lines.extend(binary_size_lines)

        if struct_def.packet_id is not None:

            packet_lines = (
                self.generate_packet_serializer(
                    struct_def
                )
            )

            lines.extend(packet_lines)

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

            if self.is_enum_type(field.field_type):

                lines.append(
                    f'        ss << "{field.name}=" '
                    f'<< static_cast<int>({field.name});'
                )
            elif self.is_vector_type(field.field_type):
                lines.append(
                    f'        ss << "{field.name}.size=" '
                    f'<< {field.name}.size();'
                )
            elif self.is_struct_type(field.field_type):

                lines.append(
                    f'        ss << "{field.name}=" '
                    f'<< {field.name}.toString();'
                )

            else:

                lines.append(
                    f'        ss << "{field.name}=" '
                    f'<< {field.name};'
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

            elif self.is_enum_type(field.field_type):
                temp_name = f"{field.name}Value"

                lines.append(
                    f"        int {temp_name} = "
                    f"static_cast<int>({field.name});"
                )

                lines.append("")

                lines.append(
                    "        out.write("
                )

                lines.append(
                    f"            reinterpret_cast<const char*>(&{temp_name}),"
                )

                lines.append(
                    f"            sizeof({temp_name})"
                )

                lines.append("        );")

                lines.append("")
            elif self.is_vector_type(field.field_type):

                inner = self.get_vector_inner_type(
                    field.field_type
                )

                lines.append(
                    f"        uint32_t {field.name}Size = "
                    f"{field.name}.size();"
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
                    f"        for (const auto& item : {field.name})"
                )

                lines.append("        {")

                if self.is_struct_type(inner):

                    lines.append(
                        "            item.serialize(out);"
                    )

                else:

                    lines.append(
                        "            out.write("
                    )

                    lines.append(
                        "                reinterpret_cast<const char*>(&item),"
                    )

                    lines.append(
                        "                sizeof(item)"
                    )

                    lines.append(
                        "            );"
                    )

                lines.append("        }")

                lines.append("")

            elif self.is_struct_type(field.field_type):

                lines.append(
                    f"        {field.name}.serialize(out);"
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

            elif self.is_enum_type(field.field_type):

                temp_name = f"{field.name}Value"

                lines.append(
                    f"        int {temp_name};"
                )

                lines.append("")

                lines.append(
                    "        in.read("
                )

                lines.append(
                    f"            reinterpret_cast<char*>(&{temp_name}),"
                )

                lines.append(
                    f"            sizeof({temp_name})"
                )

                lines.append("        );"
                )

                lines.append("")

                lines.append(
                    f"        {field.name} = "
                    f"static_cast<{field.field_type}>({temp_name});"
                )

                lines.append("")
            elif self.is_vector_type(field.field_type):
                inner = self.get_vector_inner_type(
                    field.field_type
                )

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
                    f"        for (auto& item : {field.name})"
                )

                lines.append("        {")

                if self.is_struct_type(inner):

                    lines.append(
                        "            item.deserialize(in);"
                    )

                else:

                    lines.append(
                        "            in.read("
                    )

                    lines.append(
                        "                reinterpret_cast<char*>(&item),"
                    )

                    lines.append(
                        "                sizeof(item)"
                    )

                    lines.append(
                        "            );"
                    )

                lines.append("        }")

                lines.append("")
            elif self.is_struct_type(field.field_type):
                lines.append(
                    f"        {field.name}.deserialize(in);"
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
    
    def generate_binary_size(self, struct_def):
        lines = []

        lines.append(
            "    uint32_t binarySize() const"
        )

        lines.append("    {")

        size_parts = []

        for field in struct_def.fields:
            if self.is_string_type(field.field_type):
                size_parts.append(
                    f"sizeof(uint32_t) + {field.name}.size()"
                )
            elif self.is_enum_type(field.field_type):
                size_parts.append(
                    "sizeof(int)"
                )
            elif self.is_vector_type(field.field_type):
                inner = self.get_vector_inner_type(
                    field.field_type
                )
                if self.is_struct_type(inner):
                    size_parts.append(
                        f"sizeof(uint32_t) + "
                        f"[&]()"
                        f"{{ "
                        f"uint32_t total = 0; "
                        f"for (const auto& item : {field.name}) "
                        f"{{ total += item.binarySize(); }} "
                        f"return total; "
                        f"}}()"
                    )
                else:
                    size_parts.append(
                        f"sizeof(uint32_t) + "
                        f"({field.name}.size() * sizeof({self.cpp_type(inner)}))"
                    )
            elif self.is_struct_type(field.field_type):
                size_parts.append(
                    f"{field.name}.binarySize()"
                )
            else:
                size_parts.append(
                    f"sizeof({field.name})"
                )
        if size_parts:
            lines.append("        return")
            for i, part in enumerate(size_parts):
                operator = " +"
                if i == len(size_parts) - 1:
                    operator = ";"
                lines.append(
                    f"            {part}{operator}"
                )
        else:
            lines.append("        return 0;")
        lines.append("    }")
        lines.append("")

        return lines
    
    def generate_enum(self, enum_def):
        lines = []

        lines.append(
            f"enum class {enum_def.name}"
        )

        lines.append("{")

        for i, value in enumerate(enum_def.values):

            comma = ","

            if i == len(enum_def.values) - 1:
                comma = ""

            lines.append(
                f"    {value}{comma}"
            )

        lines.append("};")
        lines.append("")

        return "\n".join(lines)
    
    def is_builtin_type(self, field_type):
        return field_type in TYPE_MAP
    
    def is_enum_type(self, field_type):
        return field_type in self.enum_names
    
    def is_struct_type(self, field_type):
        return field_type in self.struct_names
    
    def generate_default_constructor(self, struct_def):
        lines = []
        lines.append(
            f"    {struct_def.name}() = default;"
        )

        lines.append("")

        return lines

    def is_vector_type(self, field_type):
        return (
            field_type.startswith("vector<")
            and field_type.endswith(">")
        )
    
    def get_vector_inner_type(self, field_type):
        start = field_type.find("<") + 1
        end = field_type.rfind(">")
        return field_type[start:end]

    def generate_packet_serializer(
        self,
        struct_def
    ):

        lines = []

        lines.append(
            "    void serializePacket(std::ostream& out) const"
        )

        lines.append("    {")

        lines.append(
            "        PacketHeader header("
        )

        lines.append(
            "            PACKET_ID,"
        )

        lines.append(
            "            binarySize()"
        )

        lines.append(
            "        );"
        )

        lines.append("")

        lines.append(
            "        header.serialize(out);"
        )

        lines.append("")

        lines.append(
            "        serialize(out);"
        )

        lines.append("    }")

        lines.append("")

        return lines
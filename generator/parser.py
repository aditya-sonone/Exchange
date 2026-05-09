import re

from models import (
    Field,
    StructDef,
    EnumDef
)


class SchemaParser:

    STRUCT_PATTERN = re.compile(
        r"struct\s+(\w+)\s*\{(.*?)\}",
        re.DOTALL
    )

    FIELD_PATTERN = re.compile(
        r"(\w+)\s+(\w+)\s*;"
    )

    ENUM_PATTERN = re.compile(
        r"enum\s+(\w+)\s*\{(.*?)\}",
        re.DOTALL
    )

    def parse(self, text):

        structs = []

        matches = self.STRUCT_PATTERN.findall(text)

        # print("STRUCT MATCHES:", matches)

        enums = []

        enum_matches = self.ENUM_PATTERN.findall(text)

        for enum_name, body in enum_matches:

            enum_def = EnumDef(enum_name)

            values = body.split(",")

            for value in values:

                clean_value = value.strip()

                if clean_value:

                    enum_def.add_value(clean_value)

            enums.append(enum_def)

        for struct_name, body in matches:

            struct_def = StructDef(struct_name)

            fields = self.FIELD_PATTERN.findall(body)

            # print("FIELDS:", fields)

            for field_type, field_name in fields:

                field = Field(field_type, field_name)

                struct_def.add_field(field)

            structs.append(struct_def)

        return structs, enums
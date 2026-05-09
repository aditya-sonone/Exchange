import re

from models import Field, StructDef


class SchemaParser:

    STRUCT_PATTERN = re.compile(
        r"struct\s+(\w+)\s*\{(.*?)\}",
        re.DOTALL
    )

    FIELD_PATTERN = re.compile(
        r"(\w+)\s+(\w+)\s*;"
    )

    def parse(self, text):

        structs = []

        matches = self.STRUCT_PATTERN.findall(text)

        # print("STRUCT MATCHES:", matches)

        for struct_name, body in matches:

            struct_def = StructDef(struct_name)

            fields = self.FIELD_PATTERN.findall(body)

            # print("FIELDS:", fields)

            for field_type, field_name in fields:

                field = Field(field_type, field_name)

                struct_def.add_field(field)

            structs.append(struct_def)

        return structs
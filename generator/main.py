from pathlib import Path

from parser import SchemaParser
from cpp_generator import CppGenerator
from file_writer import FileWriter


def main():

    # Schema file
    schema_path = Path("../schemas/order.txt")

    # Output directory
    generated_dir = Path("../generated")

    # Read schema
    with open(schema_path, "r") as f:
        schema_text = f.read()

    # Parse schema
    parser = SchemaParser()

    structs = parser.parse(schema_text)

    # Generate C++
    generator = CppGenerator()

    # Write generated files
    writer = FileWriter(generated_dir)

    for struct_def in structs:

        generated_code = generator.generate_struct(
            struct_def
        )

        writer.write_header(
            struct_def.name,
            generated_code
        )

    print("\nGeneration complete.")


if __name__ == "__main__":
    main()
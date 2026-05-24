from pathlib import Path

from parser import SchemaParser
from cpp_generator import CppGenerator
from python_generator import PythonGenerator
from file_writer import FileWriter


def main():

    INFRASTRUCTURE_TYPES = {
        "PacketHeader"
    }
    # Schema file
    schema_path = Path("../schemas/order.txt")

    # Output directories
    cpp_generated_dir = Path(
        "../generated/cpp"
    )

    python_generated_dir = Path(
        "../generated/python"
    )

    # Read schema
    with open(schema_path, "r") as f:

        schema_text = f.read()

    # Parse schema
    parser = SchemaParser()

    structs, enums = parser.parse(
        schema_text
    )

    print(structs)

    # -----------------------------
    # C++ GENERATION
    # -----------------------------

    cpp_generator = CppGenerator()

    cpp_generator.struct_names = {
        s.name for s in structs
    }

    cpp_generator.enum_names = {
        e.name for e in enums
    }

    cpp_writer = FileWriter(
        cpp_generated_dir
    )

    # Generate C++ enums
    for enum_def in enums:

        generated_enum = (
            cpp_generator.generate_enum(
                enum_def
            )
        )

        cpp_writer.write_header(
            enum_def.name,
            generated_enum
        )

    # Generate C++ structs
    for struct_def in structs:

        generated_code = (
            cpp_generator.generate_struct(
                struct_def
            )
        )

        cpp_writer.write_header(
            struct_def.name,
            generated_code
        )

    # Generate dispatcher
    dispatcher_code = (
        cpp_generator.generate_packet_dispatcher(
            structs
        )
    )

    cpp_writer.write_header(
        "packetdispatcher",
        dispatcher_code
    )

    # -----------------------------
    # PYTHON GENERATION
    # -----------------------------

    python_generator = PythonGenerator()

    python_generator.enum_names = {
        e.name for e in enums
    }

    python_writer = FileWriter(
        python_generated_dir
    )

    # Generate Python enums
    for enum_def in enums:

        generated_enum = (
            python_generator.generate_enum(
                enum_def
            )
        )

        python_writer.write_file(
            enum_def.name.lower(),
            ".py",
            generated_enum
        )

    # Generate Python structs
    for struct_def in structs:
        if struct_def.name in INFRASTRUCTURE_TYPES:
            continue
        
        generated_code = (
            python_generator.generate_struct(
                struct_def
            )
        )

        python_writer.write_file(
            struct_def.name.lower(),
            ".py",
            generated_code
        )

    # Python package marker
    python_writer.write_file(
        "__init__",
        ".py",
        ""
    )

    registry_code = python_generator.generate_packet_registry(
        structs
    )

    python_writer.write_file(
        "packet_registry",
        ".py",
        registry_code
    )

    dispatcher_code = (
        python_generator.generate_packet_dispatcher()
    )

    python_writer.write_file(
        "packet_dispatcher",
        ".py",
        dispatcher_code
    )

    # Stamp file
    stamp_file = (
        cpp_generated_dir / ".stamp"
    )

    stamp_file.touch()

    print("\nGeneration complete.")


if __name__ == "__main__":
    main()
from pathlib import Path


class FileWriter:

    def __init__(self, output_dir):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def write_header(self, struct_name, content):

        file_name = f"{struct_name.lower()}.hpp"

        file_path = self.output_dir / file_name

        with open(file_path, "w") as f:
            f.write(content)

        print(f"Generated: {file_path}")
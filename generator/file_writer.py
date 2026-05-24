from pathlib import Path


class FileWriter:

    def __init__(self, output_dir):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def write_file(
        self,
        filename,
        extension,
        content
    ):

        file_path = (
            self.output_dir /
            f"{filename}{extension}"
        )

        with open(file_path, "w") as f:

            f.write(content)

        print(f"Generated: {file_path}")

    def write_header(
        self,
        struct_name,
        content
    ):

        self.write_file(
            struct_name.lower(),
            ".hpp",
            content
        )
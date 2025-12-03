import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    target_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
        )
    if not os.path.isfile(target_file):
        raise ValueError(f'Error: "{file_path}" is not a file')

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content = (
                    content[:MAX_CHARS]
                    + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content

    except Exception as e:
        raise ValueError(f"Error: {file_path}: {e}")

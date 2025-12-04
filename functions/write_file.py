import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating directories as needed, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    target_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
        )

    target_dir = os.path.dirname(target_file)
    os.makedirs(target_dir, exist_ok=True)

    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
            print(
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
    except Exception as e:
        raise ValueError(f"Error: Could not write to file '{file_path}': {e}")

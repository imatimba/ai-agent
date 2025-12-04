import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    target_directory = os.path.join(working_directory, directory)

    if not os.path.abspath(target_directory).startswith(
        os.path.abspath(working_directory)
    ):
        raise ValueError(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
        )
    if not os.path.isdir(target_directory):
        raise ValueError(f'Error: "{directory}" is not a directory')

    dir_contents = os.listdir(target_directory)
    files_info = ""

    try:
        for item in dir_contents:
            item_path = os.path.join(target_directory, item)
            size = os.path.getsize(item_path)
            if os.path.isdir(item_path):
                files_info += f"- {item}: file_size={size} bytes, is_dir=True\n"
            else:
                files_info += f"- {item}: file_size={size} bytes, is_dir=False\n"
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")

    return files_info

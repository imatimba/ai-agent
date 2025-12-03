import os


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

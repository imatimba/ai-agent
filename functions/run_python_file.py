import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of command-line arguments to pass to the Python file.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    target_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        raise ValueError(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        )
    if not os.path.exists(target_file):
        raise ValueError(f'Error: File "{file_path}" not found.')
    if not target_file.endswith(".py"):
        raise ValueError(f'Error: File "{file_path}" is not a Python file.')

    command = ["python", os.path.abspath(target_file)] + args

    try:
        exec_outcome = subprocess.run(
            command,
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True,
            check=True,
        )
        output = exec_outcome.stdout
        errors = exec_outcome.stderr
        result = f"STDOUT:\n{output}\nSTDERR:\n{errors}"

        if not output and not errors:
            result = "No output produced"
        if exec_outcome.returncode != 0:
            result += f"\nProcess exited with return code {exec_outcome.returncode}"

        return result

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error: executing Python file: {e}\nSTDERR:\n{e.stderr}")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Error: Python file execution timed out")
    except Exception as e:
        raise RuntimeError(f"Error: {e}")

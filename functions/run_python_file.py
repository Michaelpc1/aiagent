import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a .py python file in a specified directory relative to the working directory, executing said .py file with optional args if necessary",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file or relative path from the working directory to the file including the .py file extension",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "An optional list of args to pass to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_dir_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(work_dir_path, file_path))

        valid_target_dir = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        script = subprocess.run(command, capture_output=True, cwd=work_dir_path, text=True, timeout=30)

        result = ""
        if script.returncode != 0:
            result = f"Process exited with code {script.returncode}"
        elif script.stdout == "" and script.stderr == "":
            result = f"No output produced"
        else:
            result = f"STDOUT: {script.stdout}" + f"STDERR: {script.stderr}"

        return result


    except Exception as e:
        return f"Error: {e}"

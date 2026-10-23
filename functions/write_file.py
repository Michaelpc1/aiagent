import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a specified file relative to the working directory with the given content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the specified file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(work_dir_path, file_path))

        valid_target_dir = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"

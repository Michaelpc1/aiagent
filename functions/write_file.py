import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(work_dir_path, file_path))

        valid_target_dir = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(file_path, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"

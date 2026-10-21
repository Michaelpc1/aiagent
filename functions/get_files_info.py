import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(work_dir_path, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(target_dir)
        saved_files = []

        for file in dir_contents:
            saved_name = str(file)
            byte_count = os.path.getsize(target_dir + "/" + file)
            is_dir = os.path.isdir(target_dir + "/" + file)

            saved_files.append(f"- {saved_name}: file_size={byte_count} bytes, is_dir={is_dir}")

        return "\n".join(saved_files)
        #return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"

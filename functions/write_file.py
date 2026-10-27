import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if valid_target_file is False:
            return  f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            parent_dir = os.path.dirname(target_file)
            os.makedirs(parent_dir, exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f"Error: {e}"
import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    try:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            return  f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        else:
            dir_meta = []
            for items in os.listdir(target_dir):
                path = os.path.join(target_dir, items)
                size = os.path.getsize(path)
                if_dir = os.path.isdir(path)

                dir_meta.append(f"- {items}: file_size={size} bytes, is_dir={if_dir}")
            return "\n".join(dir_meta)



    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
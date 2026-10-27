import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:
            valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
            
            if valid_target_file is False:
                return  f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            elif os.path.isfile(target_file) is False:
                return f'Error: "{file_path}" does not exist or is not a regular file'
            elif not target_file.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'
            else:
                command = ["python", target_file]
                if args:
                    command.extend(args)
                results = subprocess.run(command, text=True, cwd=working_dir_abs, capture_output=True, timeout=30)
                
                command_output = []
                if results.returncode != 0:
                    command_output.append(f"Process exited with code {results.returncode}")
                if not results.stdout and not results.stderr:
                    command_output.append("No output produced")
                else:
                    if results.stdout:
                        command_output.append(f"STDOUT: {results.stdout}")
                    if results.stderr:
                        command_output.append(f"STDERR: {results.stderr}")

                return "\n".join(command_output)
                
    except Exception as e:
        return f"Error: executing Python file: {e}"
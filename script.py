import os
import requests
from fnmatch import fnmatch
import subprocess
from ignore import is_ignored, get_ignore_exemptions

# Replace these with your PythonAnywhere API token and username
API_TOKEN = os.environ.get("API_TOKEN")
USERNAME = os.environ.get("USERNAME")


def upload_file_to_pythonanywhere(file_path, destination_path):
    """Upload a single file to PythonAnywhere."""
    url = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{destination_path}"
    headers = {"Authorization": f"Token {API_TOKEN}"}

    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, files={"content": file})

    if response.status_code < 400:
        print(f"File '{file_path}' uploaded successfully to '{destination_path}'.")
    else:
        print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}, Response: {response.text}")



def upload_project_to_pythonanywhere(project_dir, destination_dir):
    """Upload all files in the project directory to PythonAnywhere."""
    ignored_dirs = []
    exemptions = get_ignore_exemptions(os.path.join(project_dir, ".gitignore"))

    for root, _, files in os.walk(project_dir):
        exempted = False

        for exemption in exemptions:
            index = exemption.rindex("/")
            exempt_dir = exemption[:index]
            dir = root[-len(exempt_dir):]

            if dir == exempt_dir:
                exempted = True
                break
        
        if not exempted:
            if any(root.startswith(ignored_dir) for ignored_dir in ignored_dirs):
                continue

            if is_ignored(root):
                ignored_dirs.append(root)
                continue

        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")
            relative_path = os.path.relpath(file_path, project_dir)
            destination_path = os.path.join(destination_dir, relative_path).replace("\\", "/")

            if (exempted and any(file_path[2:] == exemption for exemption in exemptions)) or not exempted:
                if not is_ignored(file_path):
                    # upload_file_to_pythonanywhere(file_path, destination_path)
                    print(f"Uploading {file_path} to {destination_path}")

                elif exempted:
                    vert = input(f"Wrong judgement? (Y/N): {file_path}: ").lower() == "n"
                    if vert:
                        # upload_file_to_pythonanywhere(file_path, destination_path)
                        print(f"Uploading {file_path} to {destination_path}")



# Example usage
project_directory = "."
destination_dir = f"/home/{USERNAME}/mysite/test"
upload_project_to_pythonanywhere(project_directory, destination_dir)
print("Done")
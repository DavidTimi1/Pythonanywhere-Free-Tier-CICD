import os
import requests
from ignore import is_ignored, get_ignore_exemptions, get_changed_files_with_tag

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
                    upload_file_to_pythonanywhere(file_path, destination_path)

                elif exempted:
                    vert = input(f"Wrong judgement? (Y/N): {file_path}: ").lower() == "n"
                    if vert:
                        upload_file_to_pythonanywhere(file_path, destination_path)


def sync_with_pythonanywhere(project_dir, destination_dir):
    """Sync the project with PythonAnywhere based on the latest commit."""
    changed_files = get_changed_files_with_tag()

    for status, file_path in changed_files:
        relative_path = os.path.relpath(file_path, project_dir)
        remote_path = os.path.join(destination_dir, relative_path).replace("\\", "/")

        print(f"Processing file '{file_path}' with status '{status}'...")
        continue

        if status == "D":
            # File was deleted locally, delete it remotely
            delete_file_from_pythonanywhere(remote_path)
        elif status in {"M", "R"}:
            # File was modified or renamed, delete the old version remotely
            delete_file_from_pythonanywhere(remote_path)
            # Upload the new version
            if not is_ignored(file_path):
                upload_file_to_pythonanywhere(file_path, remote_path)
        elif status == "A":
            # File was added locally, upload it
            if not is_ignored(file_path):
                upload_file_to_pythonanywhere(file_path, remote_path)



def delete_file_from_pythonanywhere(remote_path):
    """Delete a file from PythonAnywhere."""
    url = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path{remote_path}"
    headers = {"Authorization": f"Token {API_TOKEN}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"File '{remote_path}' deleted successfully.")
    elif response.status_code == 404:
        print(f"File '{remote_path}' not found.")
    else:
        print(f"Failed to delete file '{remote_path}'. Status code: {response.status_code}, Response: {response.text}")



# Example usage
project_directory = input("Enter the path to your project directory: ")
destination_directory = f"/home/{USERNAME}/mysite"
sync_with_pythonanywhere(project_directory, destination_directory)
print("Done")
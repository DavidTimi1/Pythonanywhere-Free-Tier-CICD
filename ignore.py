import subprocess
import os




def is_ignored(file_path):
    """Check if a file is ignored by Git using `git check-ignore`."""
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode == 0  # Return True if ignored, False otherwise
    except FileNotFoundError:
        return False  # If Git isn't installed, assume not ignored



def get_ignore_exemptions(gitignore_path=".gitignore"):
    """Check if a file is exempted from ignore based on .gitignore."""
    if not os.path.exists(gitignore_path):
        return []

    with open(gitignore_path, "r") as gitignore_file:
        exceptions = [line.strip()[1:] for line in gitignore_file if line.strip() and line.startswith("!")]

    return exceptions

def get_changed_files_with_tag(tag="[pa-CICD]"):
    """Get the list of files changed since the last commit with a specific tag in its message."""
    try:
        # Find the commit hash of the last commit with the specified tag
        result = subprocess.run(
            ["git", "log", "--grep", tag, "--format=%H", "-n", "1"],
            capture_output=True,
            text=True
        )
        last_tagged_commit = result.stdout.strip()

        if not last_tagged_commit:
            # No commit with the specified tag found, return all changes ever
            result = subprocess.run(
                ["git", "log", "--name-status", "--pretty=format:"],
                capture_output=True,
                text=True
            )
            changed_files = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    status, file_path = line.split("\t", 1)
                    changed_files.append((status, file_path))
            return changed_files

        # Get the list of changed files since the last tagged commit
        result = subprocess.run(
            ["git", "diff", "--name-status", f"{last_tagged_commit}..HEAD"],
            capture_output=True,
            text=True
        )
        changed_files = []
        for line in result.stdout.strip().split("\n"):
            if line:
                status, file_path = line.split("\t", 1)
                changed_files.append((status, file_path))
        return changed_files
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching changed files: {e}")
        return []
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
import os
import re
import subprocess

def find_and_replace(directory, old_name, new_name):
    """
    Finds and replaces occurrences of the old repository name with the new one in files within the directory.

    Args:
        directory (str): The directory to search within.
        old_name (str): The old repository name.
        new_name (str): The new repository name.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            # Replace occurrences of the old name with the new name
            content = content.replace(old_name, new_name)
            with open(file_path, 'w') as f:
                f.write(content)

def rename_repo(old_name, new_name):
    """
    Renames the repository and updates relevant files.

    Args:
        old_name (str): The old repository name.
        new_name (str): The new repository name.
    """
    # Rename the directory
    os.rename(old_name, new_name)

    # Update the remote origin
    subprocess.run(['git', 'remote', 'set-url', 'origin', f'git@github.com:{new_name}.git'], cwd=new_name)

    # Update the repository name in the README.md file
    find_and_replace(new_name, old_name, new_name)

    # Commit the changes
    subprocess.run(['git', 'add', '.'], cwd=new_name)
    subprocess.run(['git', 'commit', '-m', f'Renamed repository from {old_name} to {new_name}'], cwd=new_name)

    # Push the changes to the remote repository
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=new_name)

if __name__ == '__main__':
    old_name = input("Enter the old repository name: ")
    new_name = input("Enter the new repository name: ")

    rename_repo(old_name, new_name)

    print(f"Repository renamed from {old_name} to {new_name}.")

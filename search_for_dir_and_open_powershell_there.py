import os
import subprocess

def count_inbox_subdirs(path):
    """Counts the number of subdirectories in the 'inbox' subdirectory of the given path."""
    inbox_path = os.path.join(path, 'inbox')
    if os.path.exists(inbox_path) and os.path.isdir(inbox_path):
        return len([d for d in os.listdir(inbox_path) if os.path.isdir(os.path.join(inbox_path, d))])
    return 0

def get_sorted_directories_with_counts(base_path):
    """Returns a list of tuples (directory name, inbox count) sorted by inbox count in descending order."""
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    dir_counts = [(d, count_inbox_subdirs(os.path.join(base_path, d))) for d in dirs]
    dir_counts.sort(key=lambda x: x[1], reverse=False)
    return dir_counts

def search_for_dir_and_open_powershell():
    current_path = os.path.dirname(os.path.abspath(__file__))
    dirs_with_counts = get_sorted_directories_with_counts(current_path)

    while True:
        # Display directories with reverse numbering and sorted by subdirectory count
        for i, (d, count) in enumerate(dirs_with_counts, 1):
            print(f"{len(dirs_with_counts) - i + 1}. {d} ({count})")

        # User input
        choice = input("Enter a number or search term: ").strip()

        # Check if the input is a number and valid
        if choice.isdigit() and 1 <= int(choice) <= len(dirs_with_counts):
            selected_dir = dirs_with_counts[len(dirs_with_counts) - int(choice)][0]
            new_cwd = os.path.join(current_path, selected_dir)
            # Open PowerShell in the selected directory
            subprocess.run(["powershell.exe", "-noexit", "-command", f"cd '{new_cwd}'"], cwd=new_cwd)
            break
        else:
            # Filter directories based on the search term
            dirs_with_counts = [(d, count) for d, count in dirs_with_counts if choice.lower() in d.lower()]
            if len(dirs_with_counts) == 0:
                print("No directories found. Exiting.")
                break
            elif len(dirs_with_counts) == 1:
                # If only one directory left, open it
                selected_dir = dirs_with_counts[0][0]
                new_cwd = os.path.join(current_path, selected_dir)
                subprocess.run(["powershell.exe", "-noexit", "-command", f"cd '{new_cwd}'"], cwd=new_cwd)
                break

# Call the function
search_for_dir_and_open_powershell()


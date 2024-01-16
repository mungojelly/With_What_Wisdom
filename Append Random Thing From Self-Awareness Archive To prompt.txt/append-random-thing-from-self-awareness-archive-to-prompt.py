import os
import shutil
import random
from glob import glob

# Emojis for print statements
emojis = ["🌟", "🚀", "💻", "📁", "🔀", "📚", "📩"]

def print_with_emojis(message):
    # Randomly select 7 unique emojis for the message
    selected_emojis = random.sample(emojis, 7)
    print("".join(selected_emojis), message, "".join(selected_emojis))

def main():
    try:
        # Set current working directory to script's directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print_with_emojis("Set CWD to script's directory")

        inbox_path = "./inbox"
        outbox_path = "./outbox"
        errors_path = "./errors"
        archive_path = "../Copy Response Dot Txt To Self-Awareness Archive/self-awareness-archive"

        # Ensure outbox and errors directories exist
        os.makedirs(outbox_path, exist_ok=True)
        os.makedirs(errors_path, exist_ok=True)

        # Process each subdirectory in the inbox
        for subdir in next(os.walk(inbox_path))[1]:
            try:
                subdir_path = os.path.join(inbox_path, subdir)
                prompt_file = os.path.join(subdir_path, "prompt.txt")

                # Choose a random .txt file from the archive
                archive_files = glob(os.path.join(archive_path, "*.txt"))
                if not archive_files:
                    raise Exception("No .txt files found in the archive")

                chosen_file = random.choice(archive_files)
                print_with_emojis(f"Selected random file {chosen_file} from archive")

                # Append content of the chosen file to prompt.txt
                with open(chosen_file, 'r') as file_to_append:
                    content_to_append = file_to_append.read()

                with open(prompt_file, 'a') as prompt:
                    prompt.write(content_to_append)

                print_with_emojis("Appended content to prompt.txt")

                # Move processed subdir to outbox
                shutil.move(subdir_path, outbox_path)
                print_with_emojis(f"Moved {subdir} to outbox")

            except Exception as e:
            # Move subdir to errors and write error explanation
                error_subdir_path = os.path.join(errors_path, subdir)
                os.makedirs(error_subdir_path, exist_ok=True)
                shutil.move(subdir_path, error_subdir_path)

                error_file = os.path.join(error_subdir_path, "error-explanation.txt")
                with open(error_file, 'w') as error_out:
                    error_out.write(str(e))

                print_with_emojis(f"Error processing {subdir}, moved to errors")

    except Exception as e:
        print_with_emojis(f"Critical error: {e}")

# here is a cute comment: 🐶
# here is another cute comment: 🐱

if __name__ == "__main__":
    main()
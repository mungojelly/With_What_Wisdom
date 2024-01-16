import os
import shutil
import traceback

def print_start():
    print("🚀🌈⚡️🎬🌟 Starting process...")

def print_create_dir(dir_name):
    print(f"📁🌍🛠️🎉🔨 Creating directory: {dir_name}")

def print_copy(subdir):
    print(f"📋🤖🔁📚💼 Copied prompt-beginning.txt from genome in {subdir}")

def print_move_to_outbox(subdir):
    print(f"✅📬🚚📦🎯 Moved {subdir} to outbox")

def print_error(subdir):
    print(f"❌🚨🔥🐞💣 Error in processing {subdir}. Moved to errors.")

def print_complete():
    print("🎊🔚✨🏁🌈👽🌊🐇🕳 Process complete!")

def main():
    # Set the current working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print_start()

    inbox_path = 'inbox'
    outbox_path = 'outbox'
    error_path = 'errors'

    # Create outbox and errors directories if they don't exist
    for path in [outbox_path, error_path]:
        if not os.path.exists(path):
            os.makedirs(path)
            print_create_dir(path)

    # Process each subdirectory in the inbox
    for subdir in os.listdir(inbox_path):
        subdir_path = os.path.join(inbox_path, subdir)
        if os.path.isdir(subdir_path):
            try:
                genome_file_path = os.path.join(subdir_path, 'genome', 'prompt-beginning.txt')
                destination_file_path = os.path.join(subdir_path, 'prompt.txt')

                # Copy the prompt.txt file
                shutil.copy(genome_file_path, destination_file_path)
                print_copy(subdir)

                # Move to outbox
                shutil.move(subdir_path, outbox_path)
                print_move_to_outbox(subdir)

            except Exception as e:
                # If an error occurs, move to errors directory and create error explanation file
                error_subdir_path = os.path.join(error_path, subdir)
                shutil.move(subdir_path, error_subdir_path)
                print_error(subdir)

                error_explanation_file = os.path.join(error_subdir_path, 'error-explanation.txt')
                with open(error_explanation_file, 'w') as error_file:
                    error_file.write("Error details:\n" + traceback.format_exc())

    print_complete()

if __name__ == "__main__":
    main()

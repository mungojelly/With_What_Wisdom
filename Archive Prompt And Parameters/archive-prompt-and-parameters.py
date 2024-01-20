import os
import shutil
import time
import traceback

def cute_print(message, emojis):
    print(f"{emojis} {message} {emojis}")

def main():
    # Set the cwd to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cute_print("Setting current working directory... 🌍📂🔄", "🐾")

    inbox_path = './inbox'
    outbox_path = './outbox'
    error_path = './errors'

    # Create outbox and errors directories if they don't exist
    os.makedirs(outbox_path, exist_ok=True)
    os.makedirs(error_path, exist_ok=True)

    for subdir in os.listdir(inbox_path):
        subdir_path = os.path.join(inbox_path, subdir)
        if os.path.isdir(subdir_path):
            try:
                archive_path = os.path.join(subdir_path, 'archive')
                os.makedirs(archive_path, exist_ok=True)

                # Move and rename files
                epoch_time = str(int(time.time()))
                for file in ['prompt.txt', 'llm_parameters.json']:
                    src = os.path.join(subdir_path, file)
                    if os.path.exists(src):
                        dst = os.path.join(archive_path, f"{epoch_time}_{file}")
                        shutil.move(src, dst)
                        cute_print(f"Moved {file} to {dst} 📄➡️📂", "🚚")

                # Move processed directory to outbox
                shutil.move(subdir_path, outbox_path)
                cute_print(f"Processed {subdir}. Moved to outbox. 📤", "🎉")

            except Exception as e:
                error_file_path = os.path.join(subdir_path, 'error-explanation.txt')
                with open(error_file_path, 'w') as error_file:
                    error_file.write("Error occurred:\n")
                    error_file.write(traceback.format_exc())

                # Move to errors directory
                shutil.move(subdir_path, error_path)
                cute_print(f"Error in processing {subdir}. Moved to errors. 😿", "⚠️")

if __name__ == "__main__":
    main()

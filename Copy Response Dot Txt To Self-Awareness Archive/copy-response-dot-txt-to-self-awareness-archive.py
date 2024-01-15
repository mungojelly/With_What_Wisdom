import os
import shutil
import time

def main():
    # Set current working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("🌐 Now working from the script's own 'crib'!")

    # Paths for the directories involved
    inbox_path = './inbox'
    archive_path = './self-awareness-archive'
    outbox_path = './outbox'
    error_path = './errors'

    # Make sure our directories are ready - like a good scout!
    for path in [archive_path, outbox_path, error_path]:
        os.makedirs(path, exist_ok=True)

    # Look through each subdirectory in the inbox, like a curious cat
    for subdir in os.listdir(inbox_path):
        subdir_path = os.path.join(inbox_path, subdir)
        if os.path.isdir(subdir_path):
            try:
                # Time to play 'copy the file'!
                response_file = os.path.join(subdir_path, 'response.txt')
                archive_file = os.path.join(archive_path, f'{subdir}-{int(time.time())}.txt')
                shutil.copy2(response_file, archive_file)
                print(f"📄 Successfully archived the wise words of {subdir}.")

                # Move the subdir to the outbox - like mail, but less paper
                shutil.move(subdir_path, outbox_path)
                print(f"✅ {subdir} is now chilling in the outbox!")

            except Exception as e:
                # Oops, something broke. Time to play detective!
                error_subdir_path = os.path.join(error_path, subdir)
                shutil.move(subdir_path, error_subdir_path)
                with open(os.path.join(error_subdir_path, 'error-explanation.txt'), 'w') as error_file:
                    error_file.write(str(e))
                print(f"❌ Oopsie-daisy! We hit a snag with {subdir}: {e}")

                # Relocating the troublemaker to the error zone
                print(f"🚫 {subdir} has been banished to the land of errors!")

if __name__ == '__main__':
    main()
    print("🔍 Script has finished its adventure. Time for a coffee break? ☕")

import os
import json
import uuid
import shutil
from pathlib import Path

def print_status(message):
    emojis = ["🌟", "🚀", "✨", "🔥", "💫", "🌈", "🎉", "👏"]
    print(f"{message} {' '.join(emojis)}")

def create_or_update_relations_json(path, relations_data):
    file_path = path / 'relations.json'
    if file_path.exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
            data.update(relations_data)
    else:
        data = relations_data
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def process_directory(parent_dir, child_uuid):
    parent_plan_path = parent_dir / 'plan.json'
    child_dir = Path('outbox') / child_uuid
    child_dir.mkdir(parents=True, exist_ok=True)

    if parent_plan_path.exists():
        with open(parent_plan_path, 'r') as file:
            parent_plan = json.load(file)
        child_plan = {
            "child plan": parent_plan.get("child plan"),
            "remaining plan": parent_plan.get("child plan")
        }
        with open(child_dir / 'plan.json', 'w') as file:
            json.dump(child_plan, file, indent=4)
        # copy the parent genome directory to the child, if it's present
        parent_genome_dir = parent_dir / 'genome'
        if parent_genome_dir.exists():
            shutil.copytree(parent_genome_dir, child_dir / 'genome')

    create_or_update_relations_json(parent_dir, {"children": [child_uuid]})
    create_or_update_relations_json(child_dir, {"parent": parent_dir.name, "self": child_uuid})

    # Move the parent directory to the outbox
    shutil.move(parent_dir, Path('outbox'))
    
def main():
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)
    print_status("Changed working directory to script's location")

    inbox_path = Path('inbox')
    if not inbox_path.exists():
        print_status("No inbox directory found.")
        return

    for parent_dir in inbox_path.iterdir():
        if parent_dir.is_dir():
            child_uuid = str(uuid.uuid4())
            process_directory(parent_dir, child_uuid)
            print_status(f"Processed {parent_dir.name} into a new child directory with UUID {child_uuid}")

if __name__ == "__main__":
    main()

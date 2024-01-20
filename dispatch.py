import os
import json
import shutil

def set_cwd_to_script_dir():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("🚀 Current working directory set to the script's directory.")

def process_stations():
    for station in os.listdir('.'):
        if os.path.isdir(station):
            outbox_path = os.path.join(station, 'outbox')
            if os.path.exists(outbox_path):
                process_outbox(outbox_path, station)

def process_outbox(outbox_path, station_name):
    for subdir in os.listdir(outbox_path):
        subdir_path = os.path.join(outbox_path, subdir)
        if os.path.isdir(subdir_path):
            process_subdir(subdir_path, station_name)

def process_subdir(subdir_path, station_name):
    plan_path = os.path.join(subdir_path, 'plan.json')
    if os.path.exists(plan_path):
        with open(plan_path, 'r') as file:
            plan = json.load(file)
        
        if plan["remaining plan"]:
            destination = plan["remaining plan"].pop(0)
            print(f"📦📦📦 Moving {subdir_path} 📦📦📦 \n🚚🚚🚚 to {destination} 🚚🚚🚚")

            with open(plan_path, 'w') as file:
                json.dump(plan, file, indent=4)

            destination_inbox = os.path.join(destination, 'inbox')
            os.makedirs(destination_inbox, exist_ok=True)
            shutil.move(subdir_path, destination_inbox)
        else:
            print(f"⚠️ No remaining plan for {subdir_path}. Skipping...")

if __name__ == "__main__":
    set_cwd_to_script_dir()
    process_stations()
    print("🌟 All operations completed successfully!")

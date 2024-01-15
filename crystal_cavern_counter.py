import os

dragon_and_crystal_emojis = "💎🔮🦖🦜🦜🐉🐉"

def main():
    # Set current working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    counts = {}
    total = 0
    for root, dirs, files in os.walk("."):
        if 'inbox' in dirs:
            inbox_path = os.path.join(root, 'inbox')
            count = len(os.listdir(inbox_path))
            pool_name = os.path.basename(root)
            counts[pool_name] = count
            total += count
    # sort the counts dictionary by value
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=False)
    for pool_name, count in sorted_counts:
        print(f"{count} {pool_name} {dragon_and_crystal_emojis}")
    print(f"{total} total 🔮💀🧠")

if __name__ == "__main__":
    main()

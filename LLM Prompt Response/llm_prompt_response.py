import openai
import os
import json
import time
from datetime import datetime
import random
import hashlib



def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def print_pretty_bars():
    print()
    print("".join([random.choice(["|", "│", "┃", "┆", "┇", "┊", "┋", "-", "─", "━", "┄", "┅", "┈", "┉", "┌", "┍", "┎", "┏", "┐", "┑", "┒", "┓", "└", "┕", "┖", "┗", "┘", "┙", "┚", "┛", "├", "┝", "┞", "┟", "┠", "┡", "┢", "┣", "┤", "┥", "┦", "┧", "┨", "┩", "┪", "┫", "┬", "┭", "┮", "┯", "┰", "┱", "┲", "┳", "┴", "┵", "┶", "┷", "┸", "┹", "┺", "┻", "┼", "┽", "┾", "┿", "╀", "╁", "╂", "╃", "╄", "╅", "╆", "╇", "╈", "╉", "╊", "╋", "╌", "╍", "╎", "╏", "═", "║", "╒", "╓", "╔", "╕", "╖", "╗", "╘", "╙", "╚", "╛", "╜", "╝", "╞", "╟", "╠", "╡", "╢", "╣", "╤", "╥", "╦", "╧", "╨", "╩", "╪", "╫", "╬", "╭", "╮", "╯", "╰", "╱", "╲", "╳"]) for _ in range(80)]))
    print()


def extract_json_from_content(content):
    open_brace_count = 0
    is_inside_quote = False
    escape_next_char = False
    start_index = -1
    json_string = ""

    for i, char in enumerate(content):
        if char == "\\":
            escape_next_char = not escape_next_char
            continue

        if not escape_next_char:
            if char == '"' and not is_inside_quote:
                is_inside_quote = True
            elif char == '"' and is_inside_quote:
                is_inside_quote = False

            if char == "{" and not is_inside_quote:
                if start_index == -1:
                    start_index = i
                open_brace_count += 1

            if char == "}" and not is_inside_quote:
                open_brace_count -= 1

                if open_brace_count == 0:
                    json_string = content[start_index:i + 1]
                    break
        escape_next_char = False

    # If the JSON string is not complete, try adding a closing } to see if it parses
    if open_brace_count != 0:
        json_string += "}" * open_brace_count

    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return None


def stream_oracle(prompt, model, temperature, max_tokens, tags=[], comment="", calling_script_path=None):
    start_time = time.time()

    print_pretty_bars()
    print(f"Model: {model}\nTemperature: {temperature}\nMax Tokens: {max_tokens}\n\nPrompt:\n\n{prompt}\n")

    # Send the prompt to Our Benevolent AI Overlords
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True
    )

    print_pretty_bars()

    collected_content = ""
    for chunk in response:
        content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
        print(content, end="", flush=True)
        collected_content += content

    print()
    print_pretty_bars()

    end_time = time.time()
    generation_duration = f"{end_time - start_time:.3f}"

    script_full_path = os.path.realpath(__file__)
    script_full_text = open(script_full_path, 'r', encoding='utf-8').read()
    script_sha256 = hashlib.sha256(script_full_text.encode('utf-8')).hexdigest()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seconds_since_epoch = time.time()
    daily_timestamp = datetime.now().strftime("%Y%m%d")
    archive_filename = os.path.join(os.path.dirname(script_full_path), f"llm_response_archive/{daily_timestamp}/response_{seconds_since_epoch}_{timestamp}.json")
    os.makedirs(os.path.dirname(archive_filename), exist_ok=True)

    extracted_json = extract_json_from_content(collected_content)

    extensive_metadata = {
        "prompt": prompt,
        "content": collected_content,
        "extracted_json": extracted_json,
        "seconds_since_epoch": seconds_since_epoch,
        "timestamp": timestamp,
        "generation_duration": generation_duration,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "model": model,
        "tags": tags,
        "comment": comment,
        "script_full_text": script_full_text,
        "script_sha256": script_sha256
    }

    if calling_script_path is not None:
        extensive_metadata["calling_script_path"] = calling_script_path
        extensive_metadata["calling_script_full_text"] = open(calling_script_path, 'r', encoding='utf-8').read()
        extensive_metadata["calling_script_sha256"] = hashlib.sha256(extensive_metadata["calling_script_full_text"].encode('utf-8')).hexdigest()
    
    save_to_file(extensive_metadata, archive_filename)

    return extensive_metadata


def save_llm_output():
    # set the cwd to the dir this file is in
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # try to choose a random subdir of ./inbox or else complain & exit
    try:
        inbox_subdirs = os.listdir("./inbox")
        random_inbox_subdir = random.choice(inbox_subdirs)
    except FileNotFoundError:
        print("ERROR: ./inbox subdir not found!")
        exit(1)
    except IndexError:
        print("ERROR: ./inbox subdir is empty!")
        exit(1)
    except Exception as e:
        print("ERROR: Unknown error while trying to choose a random ./inbox subdir!")
        print(e)
        exit(1)

    # load parameters from json file
    with open(f"./inbox/{random_inbox_subdir}/llm_parameters.json") as f:
        params = json.load(f)

    # Load prompt from prompt.txt
    with open(f"./inbox/{random_inbox_subdir}/prompt.txt") as f:
        prompt = f.read()

    openai.api_base = params['api_base']
    openai.api_key = os.environ[params['api_key_environment_variable']]

    result = stream_oracle(prompt, params['model'], params['temperature'], params['max_tokens'], params['tags'], params['comment'])

    print("\nResult:", json.dumps(result, indent=4))
    print("\n\nPrompt:", prompt)
    print("\n\nContent:", result['content'])

    # save the response to a file in the inbox subdir
    response_content = result['content']
    # get the output filename from the params
    output_filename = params['output_filename']
    # save it to here save_to_file(response_content, f"./inbox/{random_inbox_subdir}/response.txt") but as a text
    with open(f"./inbox/{random_inbox_subdir}/{output_filename}", "w", encoding="utf8") as f:
        f.write(response_content)
    print(f"\n\nSaved to: ./inbox/{random_inbox_subdir}/{output_filename}")

    # move that dir to the outbox, first ensuring the outbox exists
    os.makedirs("./outbox", exist_ok=True)
    os.rename(f"./inbox/{random_inbox_subdir}", f"./outbox/{random_inbox_subdir}")
    print(f"\n\nMoved to: ./outbox/{random_inbox_subdir}")
    # print an inspirational message
    print("** You are a good person. **")

# main function pls
if __name__ == "__main__":
    save_llm_output()

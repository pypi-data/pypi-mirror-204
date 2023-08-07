import json
import os
import subprocess
import sys

import shlex
import appdirs
import openai

from pprint import pprint
DEFAULTING_MATCH = "I assume that's a NO then..."
CONFIG_FILENAME = "config.json"
DATASET_FILENAME = "dataset.json"

FORBIDDEN_COMMANDS = ["eval"]
def load_config():
    global USER_DATASET
    global USER_SHELL

    config = read_config()

    openai.api_key = config.get("OPENAI_API_KEY", "")
    if not openai.api_key:
        openai.api_key = input("Please input your OpenAI API key: ")
        try:
            openai.Model.list()
        except openai.error.AuthenticationError:
            print("The API key provided is not valid.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while checking the API key: {e}")
            sys.exit(1)
    config["OPENAI_API_KEY"] = openai.api_key
    USER_DATASET = config.get("USER_DATASET", "")
    if not USER_DATASET:
        USER_DATASET = get_config_path(DATASET_FILENAME)
        config["USER_DATASET"] = USER_DATASET
        open(USER_DATASET, "w").close()

    user_shell = subprocess.run("echo $SHELL", text=True, shell=True, capture_output=True).stdout.strip()
    USER_SHELL = os.path.basename(user_shell)
    config["USER_SHELL"] = USER_SHELL
    update_config(config)

def get_config_path(filename):
    app_name = "terminally"
    config_dir = appdirs.user_config_dir(app_name)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, filename)

def update_config(config):
    config_file = get_config_path(CONFIG_FILENAME)
    with open(config_file, "w") as f:
        json.dump(config, f)

def read_config():
    config_file = get_config_path(CONFIG_FILENAME)
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
    return config


def explain_case(prompt, command):
    try:
        explanation = explain(prompt, command)
    except openai.error.RateLimitError:
        print(" Reached the API limit, try again in a minute.")
        raise
    print("ally explains:")
    print(explanation)
    save_prompt(explanation, command, "explanation")


def explain(prompt, command):
    messages = [
        {"role": "system", "content": "Explain each part of the bash command in a list, using less than 120 tokens."},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": command}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,  # Controls the randomness of the generated text
        max_tokens=120,  # Controls the maximum length of the generated text
        n=1)
    return response.choices[0]["message"]["content"]


def promptbash_turbo(prompt):
    messages = [
        {"role": "system", "content": f"You are a CLI shell, only generate {USER_SHELL} one liners smaller than 50 tokens. DO NOT USE NATURAL LANGUAGE"},
        {"role": "user", "content": f"the bash command for {prompt} is:"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,  # Controls the randomness of the generated text
        max_tokens=50,  # Controls the maximum length of the generated text
        n=1)
    content = response.choices[0]["message"]["content"]
    # ends with "`" might be the end of a valid command 
    if content.startswith("`") and content.endswith("`"):
        content = content.strip("`")
    return content


def promptbash(prompt):
    try:
        bashcommand = promptbash_turbo(prompt)
    except openai.error.RateLimitError:
        print(" Reached the API limit, try again in a minute.")
        raise
    return bashcommand


def save_prompt(prompt, completion, return_code):
    with open(USER_DATASET, "a") as f:
        f.write(f'{{"prompt": "{prompt}", "completion": "{completion}", "return_code": "{return_code}" }}\n')


def is_valid_shell_command(command):
    try:
        parsed_command = shlex.split(command)
    except ValueError:
        return False

    if not parsed_command:
        return False

    main_command = parsed_command[0]
    if main_command in FORBIDDEN_COMMANDS:
        print(f"{main_command} is not allowed.")
        return False
    return True
    # result = subprocess.run("which " + main_command, capture_output=True, shell=True)
    # if result.returncode == 0:
    #     return True
    # print(f"Command '{parsed_command[0]}' doesn't exist in your system... ")
    # return False


def run_command(prompt, command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode:
        print(f"Returned non-zero exit code: {result.returncode}")
    # if we got here I guess the command was good and what the user wanted...
    save_prompt(prompt, command, result.returncode)
    # although there might be cases where the command is supposed to fail...


def copy_to_clipboard(command):
    if not is_valid_shell_command("xclip"):
        print("xclip not installed.")
        install_xclip = input("Run $ pacman -S xclip ? (Y/n)")
        if install_xclip in ["Y", "y", ""]:
            subprocess.run("pacman -S xclip", shell=True)
        else:
            return
    subprocess.run(
        f"echo '{command}' | xclip -selection clipboard", shell=True)
    sys.exit(0)


def roll(prompt):
    print(f"ally thinking...\n$", end="")

    try:
        command = promptbash(prompt)
    except openai.error.RateLimitError:
        sys.exit(0)

    print(f" {command}")
    if not is_valid_shell_command(command):
        return 
    choice = input(
        "[A]ccept [T]ry yours [R]eroll [C]opy to the clip-board [E]xplain command [Q]uit\n-> ").strip()
    match choice:
        case "A" | "a" | "":
            run_command(prompt, command)
        case "T" | "t":
            command = input("Enter the command you want to run: ")
            run_command(prompt, command)
        case "R" | "r":
            roll(prompt)
        case "C" | "c":
            copy_to_clipboard(command)
            sys.exit(0)
        case "E" | "e":
            try:
                explain_case(prompt, command)
            except openai.error.RateLimitError:
                sys.exit(0)
            
            choice = input(
                "[A]ccept [T]ry yours [R]eroll [C]opy to the clip-board [Q]uit\n-> ").strip()
            match choice:
                case "A" | "a" | "":
                    run_command(prompt, command)
                case "T" | "t":
                    command = input("Enter the command you want to run: ")
                    run_command(prompt, command)
                case "R" | "r":
                    roll(prompt)
                case "C" | "c":
                    copy_to_clipboard(command)
                case _:  # default & [Q]uit
                    sys.exit(0)
        case _:  # default & [Q]uit
            sys.exit(0)


def prompt_loop():
    load_config()
    while True:
        prompt = input("Prompt for command: ")
        roll(prompt)


def shell_call():
    load_config()
    prompt = " ".join(sys.argv[1:])
    roll(prompt)


def main():
    try: 
        if len(sys.argv) > 1:
            shell_call()
        else:
            prompt_loop()
    except KeyboardInterrupt:
        print("\nGoodbye by ally!")
import os
import sys
import tempfile
import subprocess
from google import genai
from pathlib import Path
# from .api_key import get_or_set_api_key
from api_key import get_or_set_api_key

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def is_git_repo() -> bool:
    path = Path(Path.cwd())
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            return True
    return False


def git_diff() -> str | None:
    try:
        result = subprocess.run(["git", "diff", "--cached"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=True)

        if not result.stdout:
            return None
        return result.stdout
    except subprocess.CalledProcessError:
        sys.exit(1)


def make_query(diff) -> str:
    prompt = f"Generate a one liner git commit message for these changes, Below are the changes:\n {diff}"
    return prompt


def generate_commit_message(diff: str) -> str:
    try:
        query = make_query(diff)
        while True:
            client = genai.Client(api_key=USER_API_KEY)
            msg = client.models.generate_content(model="gemini-2.0-flash",
                                                 contents=query)

            print(f"{GREEN}{msg.text}{RESET}")
            # generated_msg = "feat: Add poetry.lock and pyproject.toml files."
            # print(generated_msg)
            if continue_with_this_prompt(msg.text):
                break
    except genai.errors.ClientError as error:
        if error.code == 400:
            print(
                dict(
                    error=f"{RED}Gemini API key not valid, check ~/.gmsg{RESET}"
                ))
        else:
            print(error)
            sys.exit(1)


def continue_with_this_prompt(commit_msg: str) -> bool:
    action = input("Do you want to continue with this message (Y/e(edit)/n): ")
    if action in ("", "y", "Y"):
        print(f"Running: `git commit -m {commit_msg}`")
        print(
            f"{GREEN}Message commited to git, to confirm you can run git commit --amend.{RESET}"
        )
        commit_message_to_git(commit_msg)
        return True
    elif action in ("e", "E"):
        edit_message_in_editor()
    elif action in ("n", "N"):
        return False


def commit_message_to_git(generated_msg: str) -> str | None:
    try:
        result = subprocess.run(["git", "commit", "-m", generated_msg],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True,
                                text=True)

        return result.stdout
    except subprocess.CalledProcessError:
        return None


def edit_message_in_editor(initial_msg: str) -> str:
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+',
                                     delete=False) as tf:
        tf.write(initial_msg)
        tf.flush()
        temp_path = tf.name

    subprocess.run([editor, temp_path])

    with open(temp_path, 'r') as tf:
        edited_msg = tf.read().strip()

    os.unlink(temp_path)
    return edited_msg


def main():
    global USER_API_KEY

    USER_API_KEY = get_or_set_api_key()
    try:
        if not is_git_repo():
            print("Current directory does not have git initialized",
                  file=sys.stdout)
            sys.exit(1)
        diff = git_diff()
        if not diff:
            print("There's nothing in git diff.")
            sys.exit(1)

        generate_commit_message(diff)

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()

import os
import sys
import tempfile
import subprocess
from google import genai
from pathlib import Path
from .api_key import get_or_set_api_key

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


def make_query(diff: str) -> str:
    prompt = f"Generate a one liner git commit message for these changes, Below are the changes:\n {diff}"
    return prompt


def trigger_query(query: str, api_key: str) -> str:
    try:
        client = genai.Client(api_key=api_key)
        msg = client.models.generate_content(model="gemini-2.0-flash",
                                             contents=query)
        return msg.text
    except genai.errors.ClientError as error:
        if error.code == 400:
            printt(dict(error="Gemini API key not valid, check ~/.gmsg"),
                   is_success=False)
        else:
            printt(error, is_success=False)
            sys.exit(1)


def cycle_through_messages(diff: str, api_key: str) -> bool:
    query = make_query(diff)
    msg = trigger_query(query, api_key)

    while True:
        printt(msg)
        action = input(
            "Do you want to continue with this message? [Y = yes / e = edit / n = no]: "
        ).strip().lower()
        if action in ("", "y", "Y"):
            print(
                f"Running: `git commit -m {msg}`\nMessage committed to git. You can run `git commit --amend` to modify it."
            )

            commit_message_to_git(msg)
            break
        elif action in ("n", "N"):
            msg = trigger_query(query, api_key)
        elif action in ("e", "E"):
            msg = edit_message_in_editor(msg)

        else:
            print("Invalid input. Please enter 'Y', 'e', or 'n'.")


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


def printt(text: str, is_success: bool = True):
    if not is_success:
        print(RED + text + RESET, file=sys.stderr)
        return None
    print(GREEN + text + RESET)


def main():
    try:
        user_api_key = get_or_set_api_key()
        if not is_git_repo():
            printt("Not a git repository.", is_success=False)
            sys.exit(1)

        diff = git_diff()
        if not diff:
            printt("No staged changes found.", is_success=False)
            sys.exit(1)

        cycle_through_messages(diff, user_api_key)

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()

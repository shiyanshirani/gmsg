import sys
import os

from pathlib import Path


def get_or_set_api_key():
    try:
        rc = os.path.join(Path.home(), ".gmsgrc")
        if not os.path.isfile(rc):
            print(
                "Get your key from https://ai.google.dev/gemini-api/docs/api-key"
            )
            key_inp = input("Enter your Gemini API KEY: ").strip()
            with open(rc, 'w') as f:
                f.write(key_inp)

            return key_inp

        with open(rc, 'r') as f:
            return f.read().strip()
    except KeyboardInterrupt:
        sys.exit(0)

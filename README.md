# gmsg

A command-line tool that automatically generates concise and meaningful Git commit messages using Google's Gemini model based on your staged changes.

---

## 🚀 Features

* ✅ Detects if the current directory is a Git repository
* ✅ Retrieves your staged changes via `git diff --cached`
* ✅ Uses Gemini (for now) to generate a one-liner commit message
* ✅ Allows you to:

  * Accept the suggestion
  * Edit the message in your preferred text editor
  * Regenerate a new suggestion
* ✅ Automatically commits the changes with your selected message

---

## 📦 Installation

```bash
pip install gmsg
```

---

## 🛠️ Configuration

Get your [Google Gemini API key](https://aistudio.google.com/app/apikey) if you don't have already.

### 1. Set API key

Enter your api key when package is used for the first time.

```bash
$ Enter your Gemini API KEY:
```

---

## ⚙️ Usage

1. Stage your changes:

   ```bash
   git add .
   or 
   git add <file>
   ```

2. Run the package:

   ```bash
   gmsg
   ```

3. Follow the prompts:

   * Press `y/Y/enter` to commit with the suggested message
   * Press `e` to edit the message in your default `$EDITOR` (e.g., `vim`)
   * Press `n` to regenerate the commit message

---

## ✨ Example

```bash
$ git add some_file.py
$ gmsg

> Generate a one liner git commit message for these changes...
> Added error handling in API response parser

Do you want to continue with this message? [Y = yes / e = edit / n = no]: y
Running: `git commit -m Added error handling in API response parser`
Message committed to git. You can run `git commit --amend` to modify it.
```

---

## 🧩 Requirements

* Python 3.10+
* [Google Generative AI SDK](https://pypi.org/project/google-generativeai/)
* Git installed and available in your system path
---

## 📍 Roadmap

Here are some upcoming features and improvements planned for this project:

* [ ] **CLI Arguments Support**
  Add flags like `--dry-run` for non-interactive use.

* [ ] **Multi-line Commit Messages**
  Option to generate more descriptive, multi-line messages with summaries and bullet points.

* [ ] **Better Diff Parsing**
  Use syntax-aware parsing to improve prompt context and generate more accurate commit messages.

* [ ] **Git Hook Integration**
  Provide an installable Git commit hook that auto-runs this tool on `git commit`.

* [ ] **Support for Other LLMs**
  Add support for OpenAI's GPT, Claude, or local models using plugins/adapters.

---


## 📝 License

MIT License. Feel free to use, modify, and contribute!

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.


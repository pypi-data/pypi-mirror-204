# GPT-PyNvim

[![lint](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/lint.yml/badge.svg)](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/lint.yml) [![test](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/test.yml) [![linkcheck](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/JFK/gpt-pynvim-plugin/actions/workflows/linkcheck.yml) [![Downloads](https://static.pepy.tech/badge/gpt-pynvim/month)](https://pepy.tech/project/gpt-pynvim) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchainai.svg?style=social&label=Follow%20%40kiyotaman)](https://twitter.com/kiyotaman)


GPT-PyNvim is a Neovim plugin that uses OpenAI's GPT language model to generate code comments or documentation based on selected text within Neovim. This plugin requires Python 3.10 or higher.

## Directory Tree

```
gpt-pynvim/
├── autoload
│   └── gpt_pynvim.vim
└── python
    └── gpt_pynvim.py
```

## Installation

1. Clone the repository:

```
git clone https://github.com/JFK/gpt-pynvim-plugin ~/.config/nvim/plugin/gpt-pynvim
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Start Neovim.

2. Select the text you want to generate a comment or docstring for.

3. Press `,` to generate the output in a new window.

## Requirements

- Neovim
- Python 3.10 or higher

### requirements.txt

```
openai
pynvim
```

## Configuration

Ensure that your environment variable `OPENAI_API_KEY` is set to your OpenAI API key.

## Setting Up `OPENAI_API_KEY`

To set up the `OPENAI_API_KEY` environment variable, follow the instructions for your operating system:

### Linux and macOS

1. Open your terminal.

2. Open your shell profile file in a text editor. For example, if you are using the bash shell, open `~/.bashrc` or `~/.bash_profile`. If you are using the zsh shell, open `~/.zshrc`.

3. Add the following line to the file, replacing `your_api_key` with your actual OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key"
```

4. Save the file and close the text editor.

5. Restart your terminal or run `source ~/.bashrc`, `source ~/.bash_profile`, or `source ~/.zshrc` depending on the shell profile file you edited.

### Windows

1. Open the Start menu and search for "Environment Variables."

2. Click on "Edit the system environment variables."

3. In the "System Properties" window that opens, click on the "Environment Variables" button.

4. In the "Environment Variables" window, click on the "New" button under the "User variables" section.

5. Enter `OPENAI_API_KEY` as the variable name and `your_api_key` as the variable value, replacing `your_api_key` with your actual OpenAI API key.

6. Click "OK" to save the new environment variable.

7. Restart any open terminals or command prompts for the change to take effect.

Now, the `OPENAI_API_KEY` environment variable should be set and accessible to the GPT-PyNvim plugin.

## License

This project is licensed under the MIT License.

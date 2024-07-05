
# Linux Copilot

Revolutionizing Linux Development: Introducing Your Personal Linux Copilot!

Navigating complex Linux terminal commands can be challenging. Remembering every keyword and command for various tasks often becomes overwhelming. Imagine if you could simply speak to your computer and it would perform those tasks seamlessly. Now, that vision is a reality.

## Welcome to the Future: Meet Your Linux Copilot!

With the development of copilot technology for Windows and Mac OS, we have taken a significant step forward by bringing similar capabilities to Linux. You can now give your PC simple human language instructions, and it will execute everything from basic to advanced terminal commands effortlessly.

## How It Works:
By harnessing the power of Code-Llama and the Ollama-Python interface, our Linux Copilot interprets your natural language prompts and translates them into useful Linux commands. This entire process runs 100% locally on your machine.

## Agent-Centric Approach for Large Action Model Applications:
Our Linux Copilot is designed to handle more than single command execution. It employs an agent-centric approach to manage large action model applications, allowing it to perform tasks in a chain. This means it can handle complex workflows, stringing together multiple commands to accomplish intricate tasks efficiently and effectively.

## Why It’s Exciting:
- **Simplified Development**: Eliminates the need to memorize complex command chains.
- **Enhanced Productivity**: Allows you to focus on your projects while the copilot handles the commands.
- **Accessible for Everyone**: Beneficial for both beginners and experts.
- **Powerful Automation**: Capable of executing multi-step processes with a single prompt.

This is more than just a tool; it represents a significant advancement towards a future where humans and computers communicate seamlessly. It is an exciting time to be part of this technological revolution.

## Check Out the Code:
The code is available on GitHub. Dive in and start transforming the way you interact with your Linux system today.

Let’s redefine what’s possible with Linux by enabling natural language communication with your computer.

## Installation

```sh
pip install ollama
```

## Usage

### Single Command Execution
Use `test.py` to execute a single command based on the user query.

```sh
python test.py
```

### Chain Command Execution
Use `test_chain.py` to execute a series of commands based on the user query.

```sh
python test_chain.py
```

### Example

#### Single Command
```sh
Enter your terminal query (or type 'exit' to quit): list files in the current directory
Executing command: ls -l
total 4
-rw-r--r-- 1 user user 1048576 Jul  4 12:00 example.txt
```

#### Chain of Commands
```sh
Enter your terminal query (or type 'exit' to quit): update the system and list installed packages
Executing command 1: sudo apt-get update
...
Executing command 2: dpkg --list
...
```

## Functionalities

- **`test.py`**: Takes user query and executes directly a single command.
- **`test_chain.py`**: Can execute a series of commands, taking into account the output of previous commands to refine subsequent commands.

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

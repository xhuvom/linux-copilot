import ollama
import subprocess
import re

def get_terminal_commands(user_query):
    # Send the prompt to the model
    response = ollama.chat(model='codellama:7b-instruct', messages=[
        {
            'role': 'user',
            'content': f"Respond with the appropriate Linux terminal commands for the following user query. Only output the commands, without any explanations. Remove the $ sign while forming the command. If there are multiple commands to execute a task, list all the commands step by step.\nUser query: {user_query}\nCommands:",
        },
    ])

    # Extract and return the commands from the response
    commands = response['message']['content'].strip()

    # Sanitize the commands by removing unwanted characters and code block formatting
    commands = re.sub(r'[`]', '', commands)  # Remove backticks
    commands = re.sub(r'```', '', commands)  # Remove code block formatting
    commands = re.sub(r'Explanation:.*', '', commands, flags=re.DOTALL)  # Remove any explanation text if present
    commands = commands.strip()  # Remove leading/trailing whitespace

    # Ensure the commands do not contain any unwanted text
    commands = [cmd.strip() for cmd in commands.split('\n') if cmd.strip()]  # Split by lines and strip each command

    # Remove leading $ sign if present
    commands = [cmd[2:] if cmd.startswith('$ ') else cmd for cmd in commands]

    return commands

def execute_command(command):
    if not command:
        print("No command to execute.")
        return ""

    try:
        # Execute the command and capture the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        output = []
        # Stream the output line by line
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            if line:
                print(line.strip())
                output.append(line.strip())
        
        # Print any errors
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Error executing command: {stderr_output.strip()}")
            output.append(stderr_output.strip())
        
        return "\n".join(output)

    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {str(e)}")
        return str(e)

def process_commands(user_query):
    commands = get_terminal_commands(user_query)
    all_outputs = []
    
    for i, command in enumerate(commands):
        print(f"Executing command {i+1}: {command}")
        output = execute_command(command)
        all_outputs.append(output)
        
        # If there are more commands, use the output of this command to refine the next command
        if i < len(commands) - 1:
            next_query = f"{user_query}\nPrevious command output:\n{output}"
            commands[i+1:] = get_terminal_commands(next_query)

    return all_outputs

# Main function to interact with the user and get the terminal commands
def main():
    while True:
        user_query = input("What are you trying to do? (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        process_commands(user_query)

if __name__ == "__main__":
    main()


import ollama
import subprocess
import re

def get_terminal_command(user_query):
    # Send the prompt to the model
    response = ollama.chat(model='codellama:7b-instruct', messages=[
        {
            'role': 'user',
            'content': f"Respond with the appropriate Linux terminal command for the following user query. Only output and execute the command, without any explanations. Remote the $ sign while forming the command. If there are multiple commands to execute a task, then pipeline the commands and execute them step by step\nUser query: {user_query}\nCommand:",
        },
    ])

    # Extract and return the command from the response
    command = response['message']['content'].strip()

    # Sanitize the command by removing unwanted characters and code block formatting
    command = re.sub(r'[`]', '', command)  # Remove backticks
    command = re.sub(r'```', '', command)  # Remove code block formatting
    command = re.sub(r'Explanation:.*', '', command, flags=re.DOTALL)  # Remove any explanation text if present
    command = command.strip()  # Remove leading/trailing whitespace

    # Ensure the command does not contain any unwanted text
    command = command.split('\n')[0].strip()  # Take only the first line

    # Remove leading $ sign if present
    if command.startswith('$ '):
        command = command[2:]

    return command

def execute_command(command):
    if not command:
        print("No command to execute.")
        return

    try:
        # Execute the command and stream the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Stream the output line by line
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Print any errors
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Error executing command: {stderr_output.strip()}")
            # Check if the error is related to command not found
            if 'command not found' in stderr_output:
                install_and_retry(command)
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {str(e)}")

def install_and_retry(command):
    # Determine which package to install based on the command
    if 'ethtool' in command:
        install_command = "sudo apt-get install -y ethtool"
    elif 'vnstat' in command:
        install_command = "sudo apt-get install -y vnstat"
    else:
        print("Unknown command. Please install the necessary package manually.")
        return
    
    print(f"Attempting to install the necessary package with: {install_command}")
    try:
        subprocess.run(install_command, shell=True, check=True)
        print("Package installed successfully. Retrying the command...")
        execute_command(command)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package: {str(e)}")

def process_commands(commands):
    """
    Processes a list of commands and executes them one by one.
    """
    outputs = []
    for command in commands:
        if command.startswith('$ '):
            command = command[2:]
        output = execute_command(command)
        outputs.append(output)
    return outputs

# Main function to interact with the user and get the terminal command
def main():
    while True:
        user_query = input("What are you trying to do? (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        command_chain = get_terminal_command(user_query)
        commands = command_chain.split(';')
        for command in commands:
            print(f"Executing command: {command.strip()}")
            execute_command(command.strip())

if __name__ == "__main__":
    main()


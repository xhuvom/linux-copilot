import ollama
import subprocess
import re

def get_terminal_command(user_query):
    # Send the prompt to the model
    response = ollama.chat(model='codellama:7b-instruct', messages=[
        {
            'role': 'user',
            'content': f"Respond with the appropriate Linux terminal command for the following user query. Only include the command, without any explanations.\nUser query: {user_query}\nCommand:",
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

    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {str(e)}")

# Main function to interact with the user and get the terminal command
def main():
    while True:
        user_query = input("Enter your terminal query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        command = get_terminal_command(user_query)
        print(f"Executing command: {command}")
        execute_command(command)

if __name__ == "__main__":
    main()


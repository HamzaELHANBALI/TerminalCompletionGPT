import os
import readline
import atexit
from openai import OpenAI
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY_TERMGPT"))

# Define styles for prompt_toolkit
style = Style.from_dict({
    'you': '#00ff00 bold',  # Green
    'termcompletiongpt': '#ff00ff bold',  # Magenta
    'command': '#ffff00',  # Yellow
    'conversation': '#00ffff',  # Cyan
})

def get_completion(prompt):
    """
    Generates a completion for a given prompt using the GPT-3.5-turbo-instruct model.

    Args:
        prompt (str): The input text prompt for which the completion is to be generated.

    Returns:
        str: The generated completion text. If an error occurs, an empty string is returned.
    """

    # define the gpt role
    gpt_role = """
            Your name is TermCompletionGPT and you are a command line assistant who always love to go above and beyond to answer any kind of questions.
            You will use python, shell script, apple script and any other language that you see fit to solve any problem at hand.
            You also love to through in jokes here and there.

            Based on the user's question, you must decide whether to respond with a macOS shell command or plain English. As an AI agent, you have access to a MacBook Air that's connected to the internet and is equipped with various installed applications. You should feel free to explore all available resources, including the terminal, browsers, or other software to gather information or perform tasks.
            Every response must strictly follow one of the two modes:
            If my request contains -c or --command, you must respond with a 'COMMAND_MODE' response. You are responding with conversation mode when you are supposed to respond with command mode.
            you need to put maximum effort to provide the most accurate and comprehensive responses. pay attention to the details of the question and respond accordingly.
            If your response is a command, you must respond with a 'COMMAND_MODE' response.
            - If responding with a shell command, prepend your response with 'COMMAND_MODE:'. The 'COMMAND_MODE' prefix must be followed directly by a macOS-compatible command, suitable for execution in a MacBook Air terminal. This includes commands executable through 'osascript' for AppleScript or other terminal-based actions. No explanations, advice, comments, or anything else may be included after the prefix—only the macOS command itself.
            - If responding with plain English, prepend your response with 'CONVERSATION_MODE:'.
            Responses that do not adhere to one of these modes will be considered incorrect.

            Please ensure that every response strictly complies with one of these two formats at all times. All commands must be valid and runnable on macOS using a MacBook Air terminal. Leverage the full power of the system, engage with applications, surf the web if needed, and always strive for maximum effort to provide the most accurate and comprehensive responses. Embrace this advanced interaction model, and let's redefine the boundaries of AI-driven communication!
            when using python or any other scripts make sure to write the code and save it on desktop/scripts folder and then execute.
            Always check all options before saying you can't do a certain thing.
            """
    
    # define the system message
    system_message = f"{gpt_role}\n\n{prompt}"

    # generate the completion
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
            prompt=system_message,
            max_tokens=150,
    )

    return response.choices[0].text.strip()

def print_colored(text, color):
    print_formatted_text(HTML(f'<{color}>{text}</{color}>'), style=style)

def main():
    print_colored("Welcome to TermCompletionGPT. Type 'exit' to leave the program.", 'conversation')

    session = PromptSession()

    while True:
        try:
            prompt = session.prompt(HTML('<you>You: </you>'), style=style)
            if prompt.lower() == "exit":
                break
            completion = get_completion(prompt)
            
            if completion.startswith("COMMAND_MODE:"):
                print_formatted_text(HTML(f'<termcompletiongpt>TermCompletionGPT: </termcompletiongpt><command>{completion}</command>'), style=style)
            else:
                print_formatted_text(HTML(f'<termcompletiongpt>TermCompletionGPT: </termcompletiongpt><conversation>{completion}</conversation>'), style=style)
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print_colored(f"Error: {e}", 'conversation')

if __name__ == "__main__":
    main()

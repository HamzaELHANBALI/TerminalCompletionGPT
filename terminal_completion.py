import os
import readline
import atexit
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY_TERMGPT"))

# Set up readline for command history
histfile = os.path.join(os.path.expanduser("~"), ".python_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

def get_completion(prompt):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

def complete(text, state):
    if state == 0:
        readline.insert_text("")
        readline.redisplay()
        completion = get_completion(f"Generate the most probable command to autocomplete the following: {text}")
        if completion:
            return text + completion
    return None

readline.set_completer(complete)
readline.parse_and_bind("tab: complete")

print("Welcome to the AI-powered terminal autocomplete. Press Tab to autocomplete.")
print("Type 'exit' to quit.")

while True:
    try:
        command = input("$ ")
        if command.lower() == 'exit':
            break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        continue
    except EOFError:
        print("\nEOFError")
        break

print("Goodbye!")
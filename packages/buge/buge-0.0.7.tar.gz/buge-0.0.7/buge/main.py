import sys
import openai
from dotenv import load_dotenv
import os
from rich.console import Console

def main():

    load_dotenv()

    # Check if OPENAI_API_KEY is set in the environment
    if not os.getenv("OPENAI_API_KEY"):

        # Prompt user for OPENAI_API_KEY value
        openai_api_key = input("Please enter your OpenAI API key: ")

        # Write value to .env file
        env_file_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_file_path, "w") as f:
            f.write(f"OPENAI_API_KEY={openai_api_key}")
        
        load_dotenv()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    error_message = input("Please paste your error code here: ")

    console = Console()

    def get_error_explanation(error_message):
        base_prompt = (f"Explain the following error code in simple terms: `{error_message}`")
        base_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=base_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        base_response_text = base_response.choices[0].text.strip()

        # second prompt
        secondary_prompt = (f"Suggest multiple possible causes for this error code:`{error_message}`")
        secondary_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=secondary_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        secondary_response_text = secondary_response.choices[0].text.strip()

        # third prompt
        third_prompt = (f"Suggest multiple possible solutions for the following error code:`{error_message}`")
        third_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=third_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        third_response_text = third_response.choices[0].text.strip()

        print("")
        console.print('[bold]--------------------[/bold]')
        print("")
        console.print("[bold cyan]Meaning:[/bold cyan]")
        console.print(f"[green]{base_response_text}[green]")
        print("")
        console.print("[bold cyan]Possible Causes:[/bold cyan]")
        console.print(f"[green]{secondary_response_text}[green]")
        print("")
        console.print("[bold cyan]Possible Solutions:[/bold cyan]")
        console.print(f"[green]{third_response_text}[green]")
        print("")
        console.print('[bold]--------------------[/bold]')
        print("")

    get_error_explanation(error_message)

if __name__ == '__main__':
    main()
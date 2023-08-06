import typer
import os
from dotenv import load_dotenv

from search_hound_ai.hound_client_commands import HoundClientCommands

def ValidateEnv():
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY == '' or OPENAI_API_KEY == None:
        print("OPENAI_API_KEY is not set")
        exit(1)


def main():
    load_dotenv()
    app = typer.Typer(name="search_hound_ai", add_completion=True)

    app_client = HoundClientCommands(app)
    app_client()


if __name__ == "__main__":    
    ValidateEnv()
    main()


import typer
from dotenv import load_dotenv
from search_hound_ai.validate_env import ValidateEnv

from search_hound_ai.hound_client_commands import HoundClientCommands

load_dotenv()

def main():
    app = typer.Typer(name="search_hound_ai", add_completion=True)
    app_client = HoundClientCommands(app)
    app_client()


if __name__ == "__main__":    
    ValidateEnv()
    main()


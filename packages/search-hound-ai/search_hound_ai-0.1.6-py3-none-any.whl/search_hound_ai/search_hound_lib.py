import os
import typer

from search_hound_ai.openai_lib import OpenAISearch


class SearchHoundLib:
    """"Provides a simple interface to openai.

  The purpose of this simple interface is to offer a limited subset of the
  openai functionality as a command line interface.
  """

    """A quick openai implementation to search using openai."""
    def searchHound(search_string: str) -> str:
        response: str = OpenAISearch(search_string)
        return response
    def storeOpenAIConfig(config: str):
        if config is None or config == "":
            return "OPENAI_API_KEY config provided"
        
        text_file = open(".env", "w")
        text_file.write('OPENAI_API_KEY=' + config)
        text_file.close()

        return "OPENAI_API_KEY ENV saved"

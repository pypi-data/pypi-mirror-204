from search_hound_ai.openai_lib import OpenAISearch

class SearchHoundLib:
    """"Provides a simple interface to openai.

  The purpose of this simple interface is to offer a limited subset of the
  openai functionality as a command line interface.
  """

    """A quick openai implementation to search using openai."""
    def search(self, question):
        response = OpenAISearch(question)
        return response
    

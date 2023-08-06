import typer

from search_hound_ai.search_hound_lib import SearchHoundLib



def HoundClientCommands(app: typer) -> typer :
  @app.command()
  def search(query: str):
    """
    This is a fast OpenAI-based search implementation that utilizes.
    """
    search_response = SearchHoundLib.searchHound(query)
    typer.echo(search_response, err=True, color=typer.colors.YELLOW,)


  return app
"""
  Display output to the terminal using data from DailyUpdate.
"""
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table

class Display():
  """
    A wrapper class to display information from DailyUpdate
  """
  def __init__(self):
    """Initialize the Display object.

    """
    self.data = None
    self.tables = None
    self.console = Console()


  def process_data(
    self,
    data: Dict[str, List[Tuple]]) -> None:
    """Process given data.

    Store data into internal attribute
    and distribute data into different tables for displaying.
    
    Args:
      data: a dictionary of the format string and list of tuple

    data format example:
      "100 Thieves": 
      [(2023-03-01, 100 Thieves, 1, 0, Cloud 9, LCS Spring 2023)]
    """
    self.data = data
    self.tables = self.setup_tables()


  def setup_tables(self):
    """Distribute matches into tables for displaying.
    
    Two main types of tables:
      master table: all matches.
      league table: only matches for that specific league.
    """
    # List of tables to render
    tables = {}

    # Master tables to hold all results
    tables["master"] = Table(
      title="[bold color(121)]League Daily[/bold color(121)]"
      )
    tables["master"].add_column(
      "Date",
      justify="left",
      style="bold color(23)")

    tables["master"].add_column(
      "Team 1",
      justify="left",
      style="bold red")

    tables["master"].add_column(
      "Score",
      style="bold")

    tables["master"].add_column(
      "Team 2",
      justify="left",
      style="bold blue")

    tables["master"].add_column(
      "League", 
      justify="left",
      style="bold color(67)")

    # Mark repeating games
    seen = set()

    for league, matches_info in self.data.items():
      # Initialize new table if leauge is not currently in tables.
      if league not in tables:
        tables[league] = Table(
          title=f"[bold color(121)]{league}[/bold color(121)]")

        tables[league].add_column(
          "Date",
          justify="left",
          style="bold color(23)")

        tables[league].add_column(
          "Team 1",
          justify="left",
          style="bold red")

        tables[league].add_column(
          "Score",
          style="bold")

        tables[league].add_column(
          "Team 2",
          justify="left",
          style="bold blue")

        tables[league].add_column(
          "League",
          justify="left",
          style="bold color(67)")

      # Loop through list of tuples and unpack, add to table
      for match in matches_info:
        # unpack and add to table
        team_1, score_1, score_2, team_2, team_league, match_time = match
        if (team_1, score_1, score_2, team_2, match_time) not in seen:
          # Update league table
          tables[league].add_row(
            match_time,
            team_1,
            f"{score_1} - {score_2}",
            team_2,
            team_league)

          # Update master table
          tables["master"].add_row(
            match_time,
            team_1,
            f"{score_1} - {score_2}", 
            team_2,
            team_league)

          # Mark as seen to avoid repeats
          seen.add((team_1, score_1, score_2, team_2, match_time))
          seen.add((team_2, score_2, score_1, team_1, match_time))

    return tables

  def warn(self, message: str) -> None:
    """Display a warning message.

    Show a message in bold red through the console.

    Args:
      message: warning message to show
    """
    self.console.print(f"[bold red]{message}[/bold red]")

  def maximum_output_warning(self) -> str:
    """Warn about maximum output.

    Display a standard output limit message in bold red.
    """
    return (
    """
    [bold red]
    There is a 500 results per query limit from the API
    The result might be truncated.
    [/bold red]
    """
    )

  def show_master_table(self):
    """Display master table to the console.

    Show the master table with its own title.
    """
    self.console.print(self.tables["master"])

  def show_league_tables(self):
    """Display all league table to the console.

    Showing all league tables with its title,
    except for master table.
    """
    for table in self.tables:
      if table != "master":
        self.console.print(self.tables[table])

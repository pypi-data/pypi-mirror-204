"""
Typer wrapper.
"""

import sys
import typer
from datetime import datetime
from pytz import timezone
from zoneinfo import ZoneInfo
from typing import Optional, List

sys.path.insert(0, "..")

from src.daily_update import DATE, DailyUpdate
from src.display import Display
from src.util import (
  generate_general_query,
  generate_league_query,
  generate_team_query
)




app = typer.Typer()


@app.command()
def main(
    since: datetime = typer.Argument(
      DATE, help="Get result since this given [Year-Month-Day].",
      ),
    league: Optional[List[str]] = typer.Option(
      None,
      help="A specific LoL league (LCK, ...)",
      ),
    teams: Optional[List[str]] = typer.Option(
      None,
      help="A list of teams to show result for."
    )
    ):
  """
  Output table of game results.

  If date is provided, provide results
  from given date to today.

  If date is not provided, show result for the last 24 hours.

  If league is provided, only show output for matches in the given league.

  Arguments:
    since: Datetime in the format Y-M-D
    league: A league in the LoL tournament system. I.E. LCS, LCK, LPL

  """
  # Initiate objects to pull and display information
  display = Display()
  daily_update = DailyUpdate()

  # if league is provided, only provide result for that league
  if league:
    # Get data for that league specifically.
    league_query = generate_league_query(since, league)
    daily_update.get_data(league_query)

    if not daily_update.get_info():
      display.warn("No result found!")
      raise typer.Exit(0)

    display.process_data(daily_update.get_info())

    display.show_league_tables()
    display.warn(display.maximum_output_warning())

  # If teams are provided, provide results for given teams
  if teams:
    team_query = generate_team_query(since, teams)
    daily_update.get_data(team_query)

    if not daily_update.get_info():
      display.warn("No result found!")
      raise typer.Exit(0)

    display.process_data(daily_update.get_info())

    display.show_league_tables()
    display.warn(display.maximum_output_warning())

  # Only display all outputs if both teams and leagues are not provided.
  if not teams and not league:
    general_query = generate_general_query(since)

    if since == DATE:
      # Pull data and process
      daily_update.get_data(general_query)
      display.process_data(daily_update.get_info())

      # Display table
      display.show_master_table()
      display.warn(display.maximum_output_warning())
    else:
      # Convert timezone to UTC and get current time
      given_utc = since.astimezone(ZoneInfo("UTC"))
      current_utc = datetime.now(timezone("UTC"))

      # if given time > current time then abort
      # else execute, but show output limit warning
      if given_utc > current_utc:
        display.warn("Invalid date! Abort!")
        raise typer.Exit(1)
      else:
        # Pull and process data
        daily_update.get_data(general_query)
        display.process_data(daily_update.get_info())

        # Display table and warning
        display.show_master_table()
        display.warn(display.maximum_output_warning())


if __name__ == "__main__":
  app()

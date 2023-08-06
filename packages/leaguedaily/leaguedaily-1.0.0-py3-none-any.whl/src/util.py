"""
Collection of util functions.

"""
from typing import List

def generate_league_query(date: str, leagues:List[str]):
  """Generate a league specific query for data pulling.

  Args:
    date: when to pull data from
    leagues: a list of LoL league

  Returns:
    A string query to be used with Leaguepedia's LoL query.
  """
  if len(leagues) == 1:
    return f"SG.DateTime_UTC >= '{date}' AND Tournament LIKE '%{leagues[0]}%'"
  else:
    leagues_q = ""

    # Append each league into one string separate by OR
    for index, league in enumerate(leagues):
      leagues_q += f"Tournament LIKE '%{league}%'"
      if index != (len(leagues) - 1):
        leagues_q += " OR "

    return f"SG.DateTime_UTC >= '{date}' AND ({leagues_q})"

def generate_general_query(date: str):
  """ Generate a general query for data pulling.

  Pulls all matches since the given date until now.

  Args:
    date: date in string format (Year-Month-Day)

  Returns:
    A string query to be used with Leaguepedia's LoL query.
  """
  return f"SG.DateTime_UTC >= '{date}'"

def generate_team_query(date: str, teams: List[str]):
  """Generate a team specific query for data pulling.

  Args:
    date: date in string format (Year-Month-Day)
    teams: list of teams

  Returns:
    A string query to be used with Leaguepedia's LoL query.
  """
  if len(teams) == 1:
    return f"SG.DateTime_UTC >= '{date}' AND \
      (Team1='{teams[0]}' OR Team2='{teams[0]}')"
  else:
    teams_q = ""

    # Append each team into a string query seperate by OR
    for index, team in enumerate(teams):
      teams_q += f"Team1='{team}' OR Team2='{team}'"
      if index != (len(teams) - 1):
        teams_q += " OR "

    return f"SG.DateTime_UTC >= '{date}' AND ({teams_q})"

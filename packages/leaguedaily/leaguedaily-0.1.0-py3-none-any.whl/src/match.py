"""
  Blueprint/Intermediate class to store data pulled from API.
"""

class Match():
  """Match class to store data from API.

  Attributes:
    team_1: first team's name.
    team_2: second team's name.
    result: result of the match - whether team 1 wins or team 2 wins.
    leauge: the league that this match belongs to.
    match_time: time that the match occured.
  """
  def __init__(
    self,
    team_1: str,
    team_2: str,
    result: str,
    league: str,
    match_time: str) -> None:
    """Initializes the Match instance.

    Args:
      team_1: team 1 name
      team_2: team 2 name
      result: which team wins
      league: the league that this match belongs.
      match_time: when the match occured.
    """
    self.team_1 = team_1
    self.team_2 = team_2
    self.result = result
    self.league = league
    self.match_time = match_time

  def __str__(self) -> str:
    """A string representation of the result.

    """
    return f"""
    | {self.league} |
    {self.team_1} vs {self.team_2} | Result: {self.result}
    """

"""
  Represent result for a Team.
"""
class Result():
  """Result class for a Team.

  Attributes:
    opponent: Opposition team name.
    score: our record against them.
    league: the league that opponent belongs to.

  """
  def __init__(self, opponent: str, score: int, league: str, match_time: str) -> None:
    """Initializes the Result given 
    opponent's name and score against them.

    """
    self.opponent = opponent
    self.score = score
    self.league = league
    self.match_time = match_time

  def __str__(self) -> str:
    """A string representation of the result.

    """
    return f"wins against {self.opponent} with a score of {self.score}"


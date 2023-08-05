"""
  Add games to team history and get record against opponent team.

"""
import sys
sys.path.insert(0, "..")

from src.result import Result

class Team():
  """Add games to team's history and get record against other teams.

  Attributes:
    team_name: Name of the organization.
    history: List of records against opposition teams.
    league: The league that this team belongs to.

  """
  def __init__(
    self,
    team_name: str,
    league: str,
    history: dict[str, Result]) -> None:
    """Initializes the Team object.

    Args:
      team_name: name of the team.
      league: the league it belongs to 
      history: team's match history.
    """
    self.team_name = team_name
    self.history = history
    self.league = league


  def add_game(self, game: Result):
    """Add game to team's history.

    If the opponent we've already faced -> add to current 
    record against them.

    If the opponent we've not faced -> set new record against them.

    Only increase the score if we've faced opponent:
      - of the same league
      - happen on the same day

    Args:
      game: the match to update the team's history with.
    
    """
    if (game.opponent, game.league, game.match_time) in self.history:
      self.history[(game.opponent, game.league, game.match_time)] += game.score
    else:
      self.history[(game.opponent, game.league, game.match_time)] = game.score


  def get_score_against(
      self,
      opponent: str,
      league: str,
      match_time: str) -> None:
    """Get the score against opponent team.

      Get the score against opponent by looking up the team's history.

      Args:
        opponent: the opposition team to look up.
        league: the league that enemy team is in.
        match_time: time that the match occurred.

      Returns:
        Result object that contains opponent's name
        and our result against them.
    """
    return self.history[(opponent, league, match_time)]


  def __str__(self) -> str:
    """A string representation of the result.
    """
    return f"{self.team_name} result is {self.history}"

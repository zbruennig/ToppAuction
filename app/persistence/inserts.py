from typing import List

from app.mlb_models import Team

from .util import insert_result


@insert_result()
def insert_teams(teams: List[Team]):
    return teams


@insert_result()
def insert_team(team: Team):
    return team

# TODO how to gracefully handle errors?

from app.mlb_models import Team


def json_to_team(json: dict) -> Team:
    return Team(
        abbreviation=json["abbr"] if "abbr" in json else json["abbreviation"],
        name=json["name"]
    )
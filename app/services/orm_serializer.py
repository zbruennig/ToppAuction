from decimal import Decimal
from datetime import datetime

from app.mlb_models import Team, Player, CardSet, Box, BoxHistory, Pack, \
    CardType, BoxDistribution, Card, CardHistory, PhysicalCard
from app.persistence.id_fetcher import (
    get_team_id_by_name_or_abbr,
    get_card_set_id_by_name,
    get_box_id_by_name,
    get_card_type_id_by_description_and_card_set,
    get_player_id_by_name_and_team,
    get_card_id_by_description,
    get_card_id_by_player_card_set_and_card_type,
)


def optional(json: dict, key: str, default=None):
    return json[key] if key in json else default


def either_or(json: dict, key_1: str, key_2: str):
    return json[key_1] if key_1 in json else json[key_2]


def get_card_id(json: dict):
    return get_card_id_by_description(json["card"]) if "card" in json else (
        get_card_id_by_player_card_set_and_card_type(
            player=json["player"],
            team=json["team"],
            card_set=json["set"],
            card_type=json["cardType"],
        )
    )


def json_to_team(json: dict) -> Team:
    return Team(
        abbreviation=either_or(json, "abbr", "abbreviation"),
        name=json["name"],
    )


def json_to_player(json: dict) -> Player:
    return Player(
        team_id=get_team_id_by_name_or_abbr(json["team"]),
        name=json["name"],
        position=optional(json, "position"),
    )


def json_to_card_set(json: dict) -> CardSet:
    return CardSet(
        name=json["name"],  # TODO append year?
        year=json["year"],
        series=optional(json, "series"),
    )


def json_to_box(json: dict) -> Box:
    return Box(
        set_id=get_card_set_id_by_name(json["set"]),
        name=json["name"],  # TODO prepend set name?
        total_cards=either_or(json, "cards", "totalCards"),
        number_of_packs=either_or(json, "packs", "numberOfPacks"),
    )


def json_to_box_history(json: dict) -> BoxHistory:
    return BoxHistory(
        box_id=get_box_id_by_name(json["box"]),
        price=Decimal(json["price"]),
        source=optional(json, "source", default="Unknown"),
        modified_by=optional(json, "modifiedBy", default="Anonymous"),
        effective_from=optional(json, "timestamp", default=datetime.now()),
    )


def json_to_pack(json: dict) -> Pack:
    return Pack(
        box_id=get_box_id_by_name(json["box"]),
        number_of_cards=either_or(json, "cards", "numberOfCards")
    )


def json_to_card_type(json: dict) -> CardType:
    is_numbered = optional(json, "isNumbered", default=False)
    return CardType(
        set_id=get_card_set_id_by_name(json["set"]),
        description=json["description"],  # TODO prepend set name?
        number_of_players=either_or(json, "players", "numberOfPlayers"),
        is_numbered=is_numbered,
        numbered_to=either_or(json, "number", "qty") if is_numbered else None
    )


def json_to_box_distribution(json: dict) -> BoxDistribution:
    return BoxDistribution(
        box_id=get_box_id_by_name(json["box"]),
        card_type_id=get_card_type_id_by_description_and_card_set(
            description=json["cardType"],
            card_set=json["set"],
        ),
        odds=json["odds"],
    )


def json_to_card(json: dict) -> Card:
    is_numbered = optional(json, "isNumbered", default=False)
    return Card(
        player_id=get_player_id_by_name_and_team(
            name=json["player"],
            team=json["team"],
        ),
        set_id=get_card_set_id_by_name(json["set"]),
        card_type_id=get_card_type_id_by_description_and_card_set(
            description=json["cardType"],
            card_set=json["set"]
        ), # TODO could be optional?
        # TODO default based on everything?
        # {set_name + optional series} {player} {card_type}
        full_description=optional(json, "description", default=None),
        is_rookie=optional(json, "rookie"),
        # TODO pull below from CardType if it exists
        is_numbered=is_numbered,
        numbered_to=either_or(json, "number", "qty") if is_numbered else None
    )


def json_to_card_history(json: dict) -> CardHistory:
    return CardHistory(
        card_id=get_card_id(json),
        value=Decimal(json["value"]),
        source=optional(json, "source", default="Unknown"),
        modified_by=optional(json, "modifiedBy", default="Anonymous"),
        effective_from=optional(json, "timestamp", default=datetime.now()),
    )


def json_to_physical_card(json: dict) -> PhysicalCard:
    return PhysicalCard(
        card_id=get_card_id(json),
        grade=optional(json, "grade")
    )
from functools import lru_cache

from app import get_session
from app.mlb_models import Team, Player, CardSet, \
    Box, Pack, CardType, BoxDistribution, Card


@lru_cache(60)
def get_team_id_by_name_or_abbr(name: str) -> int:
    if len(name) <= 3:
        query = get_session().query(Team.id).where(Team.abbreviation == name)
    else:
        query = get_session().query(Team.id).where(Team.name == name)
    return query.scalar()


@lru_cache(1024)
def get_player_id_by_name_and_team(name: str, team: str) -> int:
    team_id = get_team_id_by_name_or_abbr(name=team)
    return get_session().query(Player.id).where(
        Player.team_id == team_id,
        Player.name == name
    ).scalar()


@lru_cache(1024)
def get_card_set_id_by_name(name: str) -> int:
    return get_session().query(CardSet.id).where(
        CardSet.name == name
    ).scalar()


@lru_cache(1024)
def get_box_id_by_name(name: str) -> int:
    return get_session().query(Box.id).where(
        Box.name == name
    ).scalar()


@lru_cache(1024)
def get_pack_id_by_box_name(box_name: str) -> int:
    box_id = get_box_id_by_name(name=box_name)
    return get_session().query(Pack.id).where(
        Pack.box_id == box_id
    ).scalar()


@lru_cache(1024)
def get_card_type_id_by_description_and_card_set(description: str, card_set: str) -> int:
    set_id = get_card_set_id_by_name(name=card_set)
    return get_session().query(CardType.id).where(
        CardType.set_id == set_id,
        CardType.description == description
    ).scalar()


@lru_cache(2048)
def get_box_distribution_id_by_box_name_and_card_type_and_set(box_name: str, card_type: str, card_set: str) -> int:
    card_type_id = get_card_type_id_by_description_and_card_set(description=card_type, card_set=card_set)
    box_id = get_box_id_by_name(name=box_name)
    return get_session().query(BoxDistribution.id).where(
        BoxDistribution.card_type_id == card_type_id,
        BoxDistribution.box_id == box_id
    ).scalar()


@lru_cache(4096)
def get_card_id_by_player_card_set_and_card_type(player: str, team: str, card_set: str, card_type: str) -> int:
    player_id = get_player_id_by_name_and_team(name=player, team=team)
    card_set_id = get_card_set_id_by_name(name=card_set)
    card_type_id = get_card_type_id_by_description_and_card_set(description=card_type, card_set=card_set)
    return get_session().query(Card.id).where(
        Card.player_id == player_id,
        Card.set_id == card_set_id,
        Card.card_type_id == card_type_id,
    ).scalar()


@lru_cache(4096)
def get_card_id_by_description(description: str) -> int:
    return get_session().query(Card.id).where(
        Card.full_description == description
    ).scalar()

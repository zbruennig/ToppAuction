# Standard Library imports
from decimal import Decimal

# Core Flask imports

# Third-party imports
from sqlalchemy import (
    Integer,
    Float,
    Column,
    String,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
)

# App imports
from app import db_manager

# alias
Base = db_manager.base


class Team(Base):
    __tablename__ = "mlb_teams"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    abbreviation: str = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Team {self.abbreviation} - {self.name}>"


class Player(Base):
    __tablename__ = "mlb_players"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    team_id: str = Column(Integer, ForeignKey("mlb_teams.id"), nullable=False)

    name: str = Column(String, nullable=False)
    position: str = Column(String, nullable=True)

    def __repr__(self):
        return f"<Player {self.id} - {self.name}>"


class CardSet(Base):
    __tablename__ = "mlb_sets"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    name: str = Column(String, nullable=False, unique=True)
    year: int = Column(Integer, nullable=False)
    series: int = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<CardSet {self.name}>"


class Box(Base):
    __tablename__ = "mlb_boxes"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)

    name: str = Column(String, nullable=False, unique=True)
    total_cards: int = Column(Integer, nullable=False)
    number_of_packs: int = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Box {self.name}>"


class BoxHistory(Base):
    __tablename__ = "mlb_box_history"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False)

    price: Decimal = Column(Numeric, nullable=False)

    source: str = Column(String, nullable=True)
    modified_by: str = Column(String, nullable=True)
    effective_from: str = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<BoxHistory {self.id}>"


class Pack(Base):
    __tablename__ = "mlb_packs"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False, unique=True)

    number_of_cards: int = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Pack {self.id}>"


class CardType(Base):
    __tablename__ = "mlb_card_types"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)

    description: str = Column(String, nullable=False)
    number_of_players: int = Column(Integer, nullable=True)
    is_numbered: bool = Column(Boolean, nullable=False)
    numbered_to: int = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<CardType {self.description}>"


class BoxDistribution(Base):
    __tablename__ = "mlb_box_distribution"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False)
    card_type_id: int = Column(Integer, ForeignKey("mlb_card_types.id"), nullable=False)

    odds: float = Column(Float, nullable=False)

    def __repr__(self):
        return f"<BoxDistribution {self.id}>"


class Card(Base):
    __tablename__ = "mlb_cards"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    player_id: int = Column(Integer, ForeignKey("mlb_players.id"), nullable=False)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)
    card_type_id: int = Column(Integer, ForeignKey("mlb_card_types.id"), nullable=True)

    full_description: str = Column(String, nullable=True, unique=True)
    is_rookie: bool = Column(Boolean, nullable=True)
    is_numbered: bool = Column(Boolean, nullable=False)
    numbered_to: int = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Card {self.id}>"


class CardHistory(Base):
    __tablename__ = "mlb_card_history"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    card_id: int = Column(Integer, ForeignKey("mlb_cards.id"), nullable=False)

    value: Decimal = Column(Numeric, nullable=False)

    source: str = Column(String, nullable=True)
    modified_by: str = Column(String, nullable=True)
    effective_from: str = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<CardHistory {self.id}>"


class PhysicalCard(Base):
    __tablename__ = "mlb_physical_cards"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    card_id: int = Column(Integer, ForeignKey("mlb_cards.id"), nullable=False)
    grade: int = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<PhysicalCard {self.id}>"

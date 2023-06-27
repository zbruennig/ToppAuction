# Standard Library imports
from decimal import Decimal

# Core Flask imports
from flask_login import UserMixin

# Third-party imports
from sqlalchemy import (
    Integer,
    Float,
    Column,
    Text,
    String,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

# App imports
from app import db_manager

# alias
Base = db_manager.base


class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    users = relationship("User", back_populates="account")


class Team(Base):
    __tablename__ = "mlb_teams"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    abbreviation: str = Column(String, nullable=False, unique=True)
    name: str = Column(String, nullable=False, unique=True)


class Player(Base):
    __tablename__ = "mlb_players"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    team_id: str = Column(Integer, ForeignKey("mlb_teams.id"), nullable=False)

    name: str = Column(String, nullable=False)
    position: str = Column(String, nullable=True)


class CardSet(Base):
    __tablename__ = "mlb_sets"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    name: str = Column(String, nullable=False, unique=True)
    year: int = Column(Integer, nullable=False)
    series: int = Column(Integer, nullable=True)


class Box(Base):
    __tablename__ = "mlb_boxes"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)

    name: str = Column(String, nullable=False)
    total_cards: int = Column(Integer, nullable=False)
    number_of_packs: int = Column(Integer, nullable=False)


class BoxHistory(Base):
    __tablename__ = "mlb_box_history"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False)

    price: Decimal = Column(Numeric, server_default="0.00")

    source: str = Column(String, nullable=True)
    modified_by: str = Column(String, nullable=True)
    effective_from: str = Column(DateTime, nullable=False)


class Pack(Base):
    __tablename__ = "mlb_packs"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False)

    number_of_cards: int = Column(Integer, nullable=False)


class CardType(Base):
    __tablename__ = "mlb_card_types"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)

    description: str = Column(String, nullable=False)
    number_of_players: int = Column(Integer, nullable=True)
    is_numbered: bool = Column(Boolean, nullable=False)
    numbered_to: int = Column(Integer, nullable=True)


class BoxDistribution(Base):
    __tablename__ = "mlb_box_distribution"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    box_id: int = Column(Integer, ForeignKey("mlb_boxes.id"), nullable=False)
    card_type_id: int = Column(Integer, ForeignKey("mlb_card_types.id"), nullable=False)

    odds: float = Column(Float, nullable=False)


class Card(Base):
    __tablename__ = "mlb_cards"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    player_id: int = Column(Integer, ForeignKey("mlb_players.id"), nullable=False)
    set_id: int = Column(Integer, ForeignKey("mlb_sets.id"), nullable=False)
    card_type_id: int = Column(Integer, ForeignKey("mlb_card_types.id"), nullable=True)

    full_description: str = Column(String, nullable=True)
    is_rookie: bool = Column(Boolean, nullable=True)
    is_numbered: bool = Column(Boolean, nullable=False)
    numbered_to: int = Column(Integer, nullable=True)


class CardHistory(Base):
    __tablename__ = "mlb_card_history"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    card_id: int = Column(Integer, ForeignKey("mlb_cards.id"), nullable=False)

    value: Decimal = Column(Numeric, server_default="0.00")

    source: str = Column(String, nullable=True)
    modified_by: str = Column(String, nullable=True)
    effective_from: str = Column(DateTime, nullable=False)


class PhysicalCard(Base):
    __tablename__ = "mlb_physical_cards"
    id: int = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    card_id: int = Column(Integer, ForeignKey("mlb_cards.id"), nullable=False)
    grade: int = Column(Integer, nullable=True)


class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRole(Base):
    __tablename__ = "users_x_roles"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(DateTime, nullable=False, server_default=func.now())


class User(UserMixin, Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(Text)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    confirmed = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    account = relationship("Account", back_populates="users")
    roles = relationship("Role", secondary="users_x_roles")

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"<User {self.email}>"

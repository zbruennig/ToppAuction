"""initial topp tables

Revision ID: 2e05d20190ef
Revises: 1_init
Create Date: 2023-06-26 05:00:14.036118+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e05d20190ef'
down_revision = '1_init'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(  # there's 30 of these
        "mlb_teams",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("abbreviation", sa.String(), nullable=False),  # BOS
        sa.Column("name", sa.String(), nullable=False),  # Boston Red Sox

        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("abbreviation"),
    )
    op.create_index("ix_mlb_teams_1", "mlb_teams", ["abbreviation", "name"])

    op.create_table(  # represents the actual human, may be on different teams in different sets if traded
        "mlb_players",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("mlb_teams.id"), nullable=False),
        sa.Column("position", sa.String(), nullable=True),
    )
    op.create_index("ix_mlb_players_1", "mlb_players", ["name", "team_id"])

    op.create_table(  # One complete collection of cards, distributed through many boxes
        "mlb_sets",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("name", sa.Integer(), nullable=False),  # full name e.g. Topps 2023 Series 1
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("series", sa.Integer(), nullable=True),
    )

    op.create_table(  # different boxes can have varying cards and different odds at rarer ones
        "mlb_boxes",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("set_id", sa.Integer(), sa.ForeignKey("mlb_sets.id")),
        sa.Column("name", sa.Integer(), nullable=False),  # e.g. 2023 Topps Baseball Series 2 - Jumbo Sealed Case

        sa.Column("total_cards", sa.Integer(), nullable=False),
        sa.Column("number_of_packs", sa.Integer(), nullable=False),
    )

    op.create_table(  # to track box price / other statistics (availability?) over time
        "mlb_box_history",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("box_id", sa.Integer(), sa.ForeignKey("mlb_boxes.id"), nullable=False),

        sa.Column("price", sa.Numeric(10, 2), server_default=sa.text("0.00")),
        sa.Column("effective_from", sa.DateTime(), nullable=False),
        sa.Column("effective_to", sa.DateTime(), nullable=False),
    )

    op.create_table(  # a box has several packs of cards, these things are in shiny plastic
        "mlb_packs",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("box_id", sa.Integer(), sa.ForeignKey("mlb_boxes.id"), nullable=False),
        sa.Column("number_of_cards", sa.Integer(), nullable=False),
    )

    op.create_table(
        "mlb_card_types",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("description", sa.String(), nullable=False),

        sa.Column("number_of_players", sa.Integer(), nullable=True),

        sa.Column("is_numbered", sa.Boolean(), nullable=False),
        sa.Column("numbered_to", sa.Integer(), nullable=True),
    )

    op.create_table(
        "mlb_box_distribution",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("box_id", sa.Integer(), sa.ForeignKey("mlb_boxes.id"), nullable=False),
        sa.Column("card_type_id", sa.Integer(), sa.ForeignKey("mlb_card_types.id"), nullable=False),

        sa.Column("odds", sa.Float(), nullable=False),
    )

    op.create_table(
        "mlb_cards",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("player_id", sa.Integer(), sa.ForeignKey("mlb_players.id"), nullable=False),
        sa.Column("set_id", sa.Integer(), sa.ForeignKey("mlb_sets.id"), nullable=False),
        sa.Column("card_type_id", sa.Integer(), sa.ForeignKey("mlb_card_types.id"), nullable=True),

        sa.Column("full_description", sa.String(), nullable=True),  # possibly used for display or price lookup

        sa.Column("is_rookie", sa.Boolean(), nullable=True),  # has RC on card
        sa.Column("is_numbered", sa.Boolean(), nullable=False),  # limited edition or not
        sa.Column("numbered_to", sa.Integer(), nullable=True),  # out of how many
    )

    op.create_table(  # to track price / possibly other statistics over time
        "mlb_card_history",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("card_id", sa.Integer(), sa.ForeignKey("mlb_cards.id"), nullable=False),

        # check resale sources, or manual input
        sa.Column("value", sa.Numeric(10, 2), server_default=sa.text("0.00")),
        sa.Column("effective_from", sa.DateTime(), nullable=False),
        sa.Column("effective_to", sa.DateTime(), nullable=False),
    )

    op.create_table(  # Will I actually use this?
        "mlb_physical_cards",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column("card_id", sa.Integer(), sa.ForeignKey("mlb_cards.id"), nullable=False),
        sa.Column("grade", sa.Integer(), nullable=True),
    )

# TODO index things


def downgrade():
    op.drop_table("mlb_physical_cards")
    op.drop_table("mlb_card_history")
    op.drop_table("mlb_box_distribution")
    op.drop_table("mlb_cards")
    op.drop_table("mlb_card_types")
    op.drop_table("mlb_packs")
    op.drop_table("mlb_box_history")
    op.drop_table("mlb_boxes")
    op.drop_table("mlb_sets")
    op.drop_table("mlb_players")
    op.drop_table("mlb_teams")


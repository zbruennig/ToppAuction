# Standard Library imports
import os
from dotenv import load_dotenv

# Core Flask imports

# Third-party imports

# App imports
from app import create_app, db_manager, mlb_models

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = create_app(os.getenv("FLASK_CONFIG") or "dev")


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db_manager,
        session=db_manager.session,
        Team=mlb_models.Team,
        Player=mlb_models.Player,
        CardSet=mlb_models.CardSet,
        Box=mlb_models.Box,
        BoxHistory=mlb_models.BoxHistory,
        Pack=mlb_models.Pack,
        CardType=mlb_models.CardType,
        BoxDistribution=mlb_models.BoxDistribution,
        Card=mlb_models.Card,
        CardHistory=mlb_models.CardHistory,
        PhysicalCard=mlb_models.PhysicalCard,
    )

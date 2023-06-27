# Standard Library imports

# Core Flask imports
from flask import Blueprint
from flask_restful import Api

# Third-party imports

# App imports
from app import db_manager
from app.api.data_routes import manual_population as manual

blueprint = Blueprint('routes', __name__)
api = Api(blueprint)

# alias
db = db_manager.session

# Request management
@blueprint.before_app_request
def before_request():
    db()


@blueprint.teardown_app_request
def shutdown_session(response_or_exc):
    db.remove()


api.add_resource(
    manual.PopulateTeams,
    manual.PopulateTeams.post_url
)

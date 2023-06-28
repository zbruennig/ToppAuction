# Standard Library imports

# Core Flask imports
from flask import Blueprint
from flask_restful import Api

# Third-party imports

# App imports
from app import get_session
from app.api.data_routes import manual_population as manual

blueprint = Blueprint('routes', __name__)
api = Api(blueprint)


# Request management
@blueprint.before_app_request
def before_request():
    get_session()()


@blueprint.teardown_app_request
def shutdown_session(response_or_exc):
    get_session().remove()


api.add_resource(
    manual.PopulateTable,
    manual.PopulateTable.post_url
)

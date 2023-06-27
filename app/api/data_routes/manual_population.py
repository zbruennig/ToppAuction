from flask import request
from flask_restful import Resource

from typing import List
from json import dumps

from app.api.util import post_response
from app.mlb_models import Team
from app.persistence.inserts import insert_teams
from app.services.orm_serializer import json_to_team
class PopulateTeams(Resource):
    post_url = "/manual/teams"

    def post(self):
        # Handle singular and lists
        body = request.json if isinstance(request.json, list) else [request.json]

        teams: List[Team] = []
        failures = []
        for json in body:
            try:
                team = json_to_team(json)
                teams.append(team)
            except Exception as e:
                # TODO proper logging
                print(f"Could not parse Team: {dumps(json)}")
                failures.append(json)
        insert_teams(teams)

        if failures:
            return post_response(f"Could not insert the following records: {dumps(failures)}", 200)
        return post_response("All records successfully added", 200)

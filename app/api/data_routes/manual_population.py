import logging

from flask import request
from flask_restful import Resource

from collections import namedtuple

from app.api.util import captures_fails, process_items
from app.persistence.inserts import insert_rows
from app.services.orm_serializer import json_to_team

logger = logging.getLogger(__name__)

Functions = namedtuple("Functions", ["convert", "insert"])


class PopulateTable(Resource):
    post_url = "/manual/<string:table>"


    def conversion_function(self, table_name):
        return {
            "teams": json_to_team
        }[table_name.lower()]

    @captures_fails()
    def post(self, table: str):
        orm_serializer = self.conversion_function(table)
        # Handle both singular and lists as lists
        jsons = request.json if isinstance(request.json, list) else [request.json]
        models, failures = process_items(jsons, orm_serializer)
        insert_rows(models)
        return failures

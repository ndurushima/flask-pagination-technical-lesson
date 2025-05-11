#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import Recipe, RecipeSchema

class Recipes(Resource):
    def get(self):
        recipes = [RecipeSchema().dump(r) for r in Recipe.query.all()]

        return recipes, 200

api.add_resource(Recipes, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
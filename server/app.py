#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import Recipe, RecipeSchema

class Recipes(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        pagination = Recipe.query.paginate(page=page, per_page=per_page, error_out=False)
        recipes = pagination.items

        return {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": [RecipeSchema().dump(recipe) for recipe in recipes]
        }, 200

api.add_resource(Recipes, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    __table_args__ = (
        db.CheckConstraint('length(instructions) >= 50'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    def __repr__(self):
        return f'<Recipe {self.id}: {self.title}>'

class RecipeSchema(Schema):
    id = fields.Int()
    title = fields.String()
    instructions = fields.String()
    minutes_to_complete = fields.Int()
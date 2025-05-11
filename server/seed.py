#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Recipe

fake = Faker()

with app.app_context():

    print("Deleting all recipes...")
    Recipe.query.delete()

    fake = Faker()

    print("Creating recipes...")
    recipes = []
    for i in range(500):
        instructions = fake.paragraph(nb_sentences=8)
        
        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15,90),
        )

        recipes.append(recipe)

    db.session.add_all(recipes)
    
    db.session.commit()
    print("Complete.")

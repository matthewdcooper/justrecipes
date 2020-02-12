import os
import psycopg2
from collections import namedtuple

Item = namedtuple('Item', 'id name')
Recipe = namedtuple('Recipe', 'id name pictures description servings preptime ingredients method')
Picture = namedtuple('Picture', 'location alt')
Ingredient = namedtuple('Ingredient', 'name category quantity')


class DB:
    def __init__(self):
        self.db_url = os.environ['DATABASE_URL']
        print(self.db_url)


    def _connect(self):
        self.conn = psycopg2.connect(self.db_url, sslmode='require')
        return self.conn.cursor()


    def _disconnect(self):
        self.conn.close()


    def _query(self, query):
        cur = self._connect()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        self._disconnect()
        return results


    def get_all_recipes(self):
        return [Item(id, name) for id, name in self._query("SELECT id, name FROM recipe;")]


    def get_ingredients_for_recipe(self, recipe_id):
        ingredients = []
        query = 'SELECT ingredient_id, quantity FROM ingredient_recipe WHERE recipe_id={}'.format(recipe_id)
        for ingredient_id, quantity in self._query(query):
            name, category = self._query('SELECT name, category FROM ingredient WHERE id={}'.format(ingredient_id))[0]
            ingredients.append(Ingredient(name, category, quantity))
        return ingredients
        #return sorted(ingredients, key=lambda i: i.category) <-- makes things worse



    def get_recipe(self, id):
        recipe_query = 'SELECT name, description, servings, preptime, method FROM recipe WHERE id={}'.format(id)
        picture_query = 'SELECT location, alt FROM picture WHERE id={}'.format(id)
        name, description, servings, preptime, method = self._query(recipe_query)[0]
        method = method.split('\n')
        pictures = [Picture(location, alt) for location, alt in self._query(picture_query)]
        ingredients = self.get_ingredients_for_recipe(id)
        return Recipe(id, name, pictures, description, servings, preptime, ingredients, method)

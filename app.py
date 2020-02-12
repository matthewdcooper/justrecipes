import os

from flask import Flask, render_template, request
from database import DB


app = Flask(__name__)
db = DB()


@app.route('/', methods=['GET'])
def index():
    recipes = db.get_all_recipes()
    return render_template('index.html', recipes=recipes)


@app.route('/recipe', methods=['GET'])
def recipe():
    id = request.args.get('id')
    recipe = db.get_recipe(id)
    return render_template('recipe.html', recipe=recipe)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    elif request.method == 'POST':
        print('# Recipe Submission')
        print('## Picture')
        print(request.files['picture'].read())
        print('## Ingredients')
        print(request.form['ingredients'])
        print('## Method')
        print(request.form['method'])
        return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)

import requests
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"


class CountryInput(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CountryInput()
    if form.validate_on_submit():
        country = form.country.data
        url = "https://www.themealdb.com/api/json/v1/1/filter.php"
        params = {
            "a": country
        }

        responses = requests.get(url=url,  params=params).json()["meals"]

        return render_template("response.html", responses=responses)

    return render_template("index.html", form=form)


@app.route('/meal')
def meal():
    meal_id = request.args.get("id")
    url = "https://www.themealdb.com/api/json/v1/1/lookup.php"
    params = {
        "i": meal_id
    }
    response = requests.get(url=url, params=params).json()["meals"][0]
    ingredient_list = []
    for num in range(1, 21):
        meal_ingredient = response[f"strIngredient{num}"]
        meal_measurement = response[f"strMeasure{num}"]
        if meal_ingredient is None:
            break
        ingredient_list.append(f"{meal_ingredient} - {meal_measurement}")

    return render_template("meal.html", response=response, ingredients=ingredient_list)


if __name__ == "__main__":
    app.run(debug=True)
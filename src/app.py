import sqlite3
import os
import pathlib
from typing import Dict, Union

from flask import Flask
from flask import render_template, redirect, url_for

from config import DEBUG
from db.db import DB
from moon_phases import moon_phases_by_years
from moon_phase import moon_phase_dict
from ma_fonction import list_deces_prematures


app: Flask = Flask(__name__)

db: DB = DB(os.path.join(pathlib.Path(__file__).parent.absolute(), "db/database.db"))


@app.route("/")
@app.route("/index")
def index():
    """
    Render the index html page
    """
    births_moon_cycle_by_year: Dict[int, str] = moon_phases_by_years(db.get_births())
    graph_data: Dict[str, Union[list, dict]] = {"birth_moon_label": list(moon_phase_dict.values()), "birth_moon_by_years": births_moon_cycle_by_year, "deaths": list_deces_prematures()}
    return render_template("index.html", graph_data=graph_data)


@app.route('/about')
def about():
    """
    Render the about page
    """
    return render_template("about.html")


@app.route('/favicon.ico')
def favicon():
    """
    Redirect to the favicon
    """
    return redirect(url_for('static', filename='images/favicon.png'))

@app.errorhandler(404)
def not_found(e):
    """
    Render the 404 page
    """
    return render_template("404.html"), 404



if __name__ == "__main__":
    app.run(debug=DEBUG)
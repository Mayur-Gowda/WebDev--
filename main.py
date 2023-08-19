from flask import Flask, render_template, request
from datetime import date
from scrape import get_blogs, get_quote
from flask_sqlalchemy import SQLAlchemy
import secrets

year = date.today().year

app = Flask(__name__)
app.config["SECRET_KEY"] = "@0thisisaSECRET_KEY0@"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

db = SQLAlchemy()
db.init_app(app)


class Donator(db.Model):
    __tablename__ = 'donators'
    unique = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String)


with app.app_context():
    db.create_all()

quotes = get_quote()


@app.route('/')
def homepage():
    return render_template("home.html", year=year, quotes=quotes)


@app.route('/our-work')
def work():
    return render_template('work.html', year=year)


@app.route('/reports&news')
def randn():
    dt = get_blogs()
    return render_template('randn.html', year=year, dt=dt)


@app.route('/get-involved')
def involve():
    return render_template('involve.html', year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)


@app.route('/donate')
def donate():
    return render_template('donate.html', year=year)


@app.route('/payment', methods=['POST', "GET"])
def payment():
    if request.method == "POST":
        form_action = str(request.form.get('firstName'))

    return render_template('payment.html', year=year)


if __name__ == "__main__":
    app.run(debug=True)


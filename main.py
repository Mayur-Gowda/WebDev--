from flask import Flask, render_template, redirect
from datetime import date
from scrape import get_blogs, get_quote

year = date.today().year

app = Flask(__name__)


@app.route('/')
def homepage():
    quote, author = get_quote()
    return render_template("home.html", year=year, quote=quote,author=author)


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


@app.route('/payment')
def payment():
    return render_template('payment.html', year=year)


if __name__ == "__main__":
    app.run(debug=True)


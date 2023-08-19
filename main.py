from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from scrape import get_blogs, get_quote
from flask_sqlalchemy import SQLAlchemy

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
    data = Donator.query.all()
    return render_template('donate.html', year=year, data=data)


@app.route('/payment', methods=['POST', "GET"])
def payment():
    if request.method == "POST":
        unique_id = str(request.form.get('uniqueID'))
        user = Donator.query.filter_by(unique=unique_id).first()
        f_name = str(request.form.get('firstName'))
        l_name = str(request.form.get('lastName'))
        name = f"{f_name} {l_name}"
        amount = int(request.form.get('amount'))
        email = str(request.form.get('email'))
        if user is None:
            user_data = Donator(
                unique=unique_id,
                name=name,
                amount=amount,
                email=email
            )
            db.session.add(user_data)
            db.session.commit()
            return redirect(url_for('donate'))
        else:
            user.amount += amount
            db.session.commit()
            return redirect(url_for('donate'))
    return render_template('payment.html', year=year)


if __name__ == "__main__":
    app.run(debug=True)


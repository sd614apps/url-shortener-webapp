from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String())
    short_url = db.Column(db.String(10), unique=True)

with app.app_context():
    db.create_all()


# Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        new_url = URL(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('success.html', short_url=short_url)
    return render_template('index.html')

@app.route("/<short_url>")
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.long_url)
    return "URL not found"

if __name__ == '__main__':
    app.run(debug=True)

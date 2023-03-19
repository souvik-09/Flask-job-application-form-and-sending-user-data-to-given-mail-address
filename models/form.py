from config import db

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(50))
    
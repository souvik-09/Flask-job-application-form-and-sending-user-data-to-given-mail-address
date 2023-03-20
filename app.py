from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from models.form import Form
from config import db, SECRET_KEY
from flask_mail import Mail, Message
from os import environ, path, getcwd
from dotenv import load_dotenv

load_dotenv(path.join(getcwd(), '.env'))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI') 
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_USERNAME"] = environ.get('MAIL_USERNAME') 
    app.config["MAIL_PASSWORD"] = environ.get('MAIL_PASSWORD') 
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Successfully")
    
    mail = Mail(app)


    with app.app_context():
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                date = request.form['date']
                occupation = request.form['occupation']
                
                form = Form(first_name=first_name, last_name=last_name,
                            email=email, date=date,occupation=occupation)
                db.session.add(form)
                db.session.commit()
                
                message_body = f"Thank you for your submission, {first_name}. \n " \
                                f"Here are your data: \n {first_name} {last_name} \n"  \
                                    f"Your occupation: {occupation} \n " \
                                     f"Your joining date is: {date} \n " \
                                        f"Thank you!"
                message = Message(subject="New form submission",
                                  sender=app.config["MAIL_USERNAME"],
                                  recipients=[email],
                                  body=message_body)
                
                mail.send(message)
                
                flash(f"{first_name}, Your form was submitted successfully!", "success")
                
            return render_template("index.html")


        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
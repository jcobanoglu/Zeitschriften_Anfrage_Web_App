from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators


# create a flask instance 
app = Flask(__name__)
# add secret_key
app.secret_key = "secret"
# add database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize the database 
db = SQLAlchemy(app)

# create model 
class Users(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    library = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True) #unique  = one person/one mail 
    online = db.Column(db.String(9), nullable=False)
    print = db.Column(db.String(9), nullable=False)
    message = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # create a string
    def __repr__(self):
        return '<Users %r>' % self.name

# create a form class 
class UserForm(FlaskForm):
    name = StringField("Name*", [validators.DataRequired()])
    library = StringField("Einrichtung/Bibliothek*", [validators.DataRequired()])
    email = StringField("E-Mail*", [validators.DataRequired()])
    online = StringField("Online ISSN", [validators.optional(), validators.length(max=9)])
    print = StringField("Print ISSN", [validators.optional(), validators.length(max=9)])
    message = TextAreaField("Anmerkung zur Zeitschrift", [validators.optional(), validators.length(max=300)])
    submit = SubmitField("Senden")


@app.route("/", methods=['GET','POST'])
def formular():
    name = None 
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: 
            user = Users(name=form.name.data, library=form.library.data, email=form.email.data, 
            online=form.online.data, print=form.print.data, message=form.message.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        form.name.data = ''
        form.library.data = ''
        form.email.data = ''
        form.online.data = ''
        form.print.data = ''
        form.message.data = ''
        flash('Vielen Dank! Ihre Anfrage war efolgreich!')
    return render_template("formular.html", 
        name=name,
        form=form)
    
@app.route("/aktuelles")
def aktuelles():
    name = None 
    form = UserForm()            
    our_users = Users.query.order_by(Users.date_added)
    return render_template("aktuelles.html",
        name=name,
        form=form, 
        our_users=our_users)


if __name__ == "__main__":
    app.run(debug=True)

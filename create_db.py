from Geoguesser import create_app, db, bcrypt

from Geoguesser.models import User

app = create_app()  
app.app_context().push()

db.drop_all()
db.create_all()

user = User(
    firstname='Gurman',
    lastname='Dhaliwal',
    alias='don',
    email='gs42.dhaliwal@surreyschools.ca',
    password=bcrypt.generate_password_hash('p@ssw0rd')
)
db.session.add(user)
db.session.commit()
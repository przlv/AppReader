from reader import app, db

with app.app_context():
        db.create_all()
        db.drop_all()
        db.create_all()
from reader import app, db
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Book(db.Model):
    id: int
    title: str
    author: str
    genre: str
    cover: str
    rating: int
    description: str
    notes: str
    year_publication: str
    price: str
    sale: bool
    weight: int
    page_count: int
    price_type: bool
    library_text: str
    affinity: str
    count: int
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer)
    cover = db.Column(db.String(50), nullable=False, default='default.jpg')
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    year_publication = db.Column(db.Date())
    price = db.Column(db.Float)
    sale = db.Column(db.Boolean)
    weight = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    price_type = db.Column(db.Boolean)
    library_text = db.Column(db.String(1000), nullable=False)
    affinity = db.Column(db.String(250), nullable=False)
    count = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Book {self.title}>'

@dataclass
class Author(db.Model):
    id: int
    first_name: str
    surname: str
    last_name: str
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f'<Author {self.first_name} {self.surname} {self.last_name}>'

@dataclass
class Genre(db.Model):
    id: int
    name: str
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'

@dataclass
class Delivery(db.Model):
    id: int
    date: str
    count: str
    description: str
    weight: str
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True),
                    server_default=func.now())
    count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Delivery {self.id} {self.date}>'

@dataclass
class Client(db.Model):
    id: int
    first_name: str
    surname: str
    last_name: str
    last_logon: str
    phone: str
    zipcode: str
    password: str
    email: str
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    last_logon = db.Column(db.DateTime(timezone=True))
    phone = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Client {self.id}>'

@dataclass
class Admin(db.Model):
    id: int
    first_name: str
    surname: str
    last_name: str
    last_logon: str
    reg_date: str
    phone: str
    zipcode: str
    password: str
    login: str
    email: str
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    last_logon = db.Column(db.DateTime(timezone=True))
    reg_date = db.Column(db.DateTime(timezone=True),
                    server_default=func.now())
    phone = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.id} {self.first_name}>'
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER,DateTime
from reader import app, db
from dataclasses import dataclass

@dataclass #Book Table
class Book(db.Model):
    book_id: int
    title: str
    cover: str
    rating: int
    description: str
    notes: str
    created_at : str
    year_publication: date
    price: float
    sale: bool
    weight: int
    page_count: int
    price_type: bool
    library_text: str
    affinity: str
    count: int
    #Foreign Keys 
    author_id: int
    genre: int
    publish_id : int
    type_id : int 
    level_id: int  

    #initialization of the book database fields 
    book_id = db.Column(INTEGER, primary_key=True) 
    title = db.Column(INTEGER, unique=True, nullable=False)
    rating = db.Column(FLOAT)
    cover = db.Column(db.String(100), nullable=False, default='default.jpg')
    description = db.Column(db.String(1000))
    notes = db.Column(db.String(1000))
    created_at = created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    year_publication = db.Column(DATE)
    price = db.Column(FLOAT)
    sale = db.Column(BOOLEAN)
    weight = db.Column(INTEGER)
    page_count = db.Column(INTEGER)
    price_type = db.Column(BOOLEAN)
    library_text = db.Column(db.String(1000))
    affinity = db.Column(db.String(250))
    count = db.Column(INTEGER)
    #initialization of Foreign Keys 
    author_id = db.Column(INTEGER , nullable=False)
    genre = db.Column(INTEGER, nullable=False)
    publish_id = db.Column(INTEGER, nullable=False)
    type_id = db.Column(INTEGER, nullable=False)
    level_id = db.Column(INTEGER, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

@dataclass# Author Table
class Author(db.Model):
    author_id: int
    first_name: str
    surname: str
    last_name: str
    cover : str

    #initialization of the author database fields 
    author_id = db.Column(INTEGER, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(100), nullable=False, default='default.jpg')

    def __repr__(self):
        return f'<Author {self.first_name} {self.surname} {self.last_name}>'

@dataclass # Genre Table
class Genre(db.Model):
    genre_id: int
    name: str
    
    #initialization of the genre database fields 
    genre_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'

@dataclass # Delivery Table
class Delivery(db.Model):
    delivery_id: int
    date: DateTime
    count: int
    description: str
    weight: int
    #Foreign Key 
    client_id : int
    
    #initialization of the Delivery database fields 
    delivery_id = db.Column(INTEGER, primary_key=True)
    date = db.Column(DATETIME)
    count = db.Column(INTEGER, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    weight = db.Column(INTEGER, nullable=False)
    #initialization of Foreign Key 
    client_id = db.Column(INTEGER, nullable=False)

    def __repr__(self):
        return f'<Delivery {self. delivery_id} {self.date}>'

@dataclass #Client Table
class User(db.Model):
    user_id: int
    first_name: str
    surname: str
    last_name: str
    last_logon: DateTime
    phone: str
    zipcode: str
    address: str
    email : str
    login: str
    password: str
    RegDate: DateTime
    UserType : str
    
    #initialization of the Client database fields 
    user_id = db.Column(INTEGER, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    last_logon = db.Column(DATETIME, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    RegDate = db.Column(DATETIME, nullable=False)
    UserType = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<Client {self.user_id}{self.first_name}>'

@dataclass #Publish Table
class Publish(db.Model):
    publish_id: int
    name: str 

    #initialization of the Publish database fields
    publish_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Publish {self.name}>'

@dataclass # PubType Table
class Type(db.Model):
    type_id: int
    name: str 

    #initialization of the Type database fields
    type_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Type {self.name}>'

@dataclass # EdLevel Table
class Level(db.Model):
    Level_id: int
    name: str 

    #initialization of the Level database fields
    Level_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Level {self.name}>'
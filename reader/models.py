#database and display model relationship
from cgitb import text
from datetime import date
from pickletools import int4
import string
from tokenize import String
from typing import Text
from sqlalchemy import BOOLEAN, DATE, DATETIME, FLOAT, INTEGER, Boolean, Date, DateTime, Float, Integer
from reader import app, db
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Book(db.Model):
    book_id: int
    title: str
    cover: str
    rating: int
    description: str
    notes: str
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
    genre_id: int
    publish_id : int
    type_id : int 
    level_id: int  

    #initialization of the book database fields 
    book_id = db.Column(INTEGER, primary_key=True) 
    title = db.Column(INTEGER, unique=True, nullable=False)
    rating = db.Column(FLOAT)
    cover = db.Column(db.String(100), nullable=False, default='default.jpg')
    description = db.Column(Text)
    notes = db.Column(Text)
    year_publication = db.Column(DATE)
    price = db.Column(FLOAT)
    sale = db.Column(BOOLEAN)
    weight = db.Column(INTEGER)
    page_count = db.Column(INTEGER)
    price_type = db.Column(BOOLEAN)
    library_text = db.Column(db.String(1000), nullable=False)
    affinity = db.Column(db.String(250), nullable=False)
    count = db.Column(INTEGER)
    #initialization of Foreign Keys 
    author_id = db.Column(INTEGER , nullable=False)
    genre_id = db.Column(INTEGER, nullable=False)
    publish_id = db.Column(INTEGER, nullable=False)
    type = db.Column(INTEGER, nullable=False)
    level = db.Column(INTEGER, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

@dataclass# Author Table
class Author(db.Model):
    author_id: int
    first_name: str
    surname: str
    last_name: str
    
    #initialization of the author database fields 
    author_id = db.Column(INTEGER, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

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
class Client(db.Model):
    client_id: int
    first_name: str
    surname: str
    last_name: str
    last_logon: DateTime
    phone: str
    zipcode: str
    password: str
    email: str
    
    #initialization of the Client database fields 
    client_id = db.Column(INTEGER, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    last_logon = db.Column(DATETIME, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Client {self.client_id}>'

@dataclass #Administrator Table
class Admin(db.Model):
    admin_id: int
    first_name: str
    surname: str
    last_name: str
    last_logon: DateTime
    reg_date: DateTime
    phone: str
    zipcode: str
    password: str
    login: str
    email: str
    
    #initialization of the Admin database fields 
    admin_id= db.Column(INTEGER, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    last_logon = db.Column(DATETIME, nullable=False)
    reg_date = db.Column(DATETIME, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Admin {self. admin_id} {self.first_name}>'

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
        return f'<Publish {self.name}>'

@dataclass # EdLevel Table
class Level(db.Model):
    Level_id: int
    name: str 

    #initialization of the Level database fields
    Level_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Level {self.name}>'
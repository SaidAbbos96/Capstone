# imports
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Numeric, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']
#local db url set DATABASE_URL=postgresql://postgres:1111@localhost:5432/capstone
db = SQLAlchemy()

# setup db
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# table restaurants
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    owner_id = Column(String, nullable=False)  # owner_id will be retrieved from token to see which user owns the restaurant
    reservation_rel = db.relationship('Reservations', backref='restaurnt_res', lazy=True)
    reservation_rel = db.relationship('MenuItems', backref='restaurnt_menu_item', lazy=True)  

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
             "name": self.name
            ,"address": self.address
        }


# Table to store information about the reservations at restaurants
class Reservations(db.Model):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    time_of_res = Column(DateTime)
    num_of_people = Column(Integer)
    name_for_res = Column(String) 
    customer_id = Column(String) # customer_id will be retrieved from token
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
             "time_of_res": self.time_of_res
            ,"num_of_people": self.num_of_people
            ,"restaurant_name": self.restaurnt_res.name
        } 



# Table to store information about the Menu Items at restaurants
class MenuItems(db.Model):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
             "name": self.name
            ,"description": self.description
            ,"price": str(self.price)
            ,"restaurant_name": self.restaurnt_menu_item.name
        }
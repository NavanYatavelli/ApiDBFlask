""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the BreakingNews class to manage actions in the 'news' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class BreakingNews(db.Model):
    __tablename__ = 'breakingnews'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), unique=False, nullable=False)
    _network = db.Column(db.String(255), unique=False, nullable=False)
    _day = db.Column(db.Date)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, title, network, day=date.today()):
        self._title = title    # variables with self prefix become part of the object, 
        self._network = network
        self._day = day

    # a name getter method, extracts name from object
    @property
    def title(self):
        return self._title
    
    # a setter function, allows name to be updated after initial object creation
    @title.setter
    def title(self, title):
        self._title = title
    
    # a getter method, extracts email from object
    @property
    def network(self):
        return self._network
    
    # a setter function, allows name to be updated after initial object creation
    @network.setter
    def network(self, network):
        self._network = network
        
    # check if uid parameter matches user id in object, return boolean
    def is_network(self, network):
        return self._network == network
      
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def day(self):
        day_string = self._day.strftime('%m-%d-%Y')
        return day_string
    
    # dob should be have verification for type date
    @day.setter
    def day(self, day):
        self._day = day
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._day.year - ((today.month, today.day) < (self._day.month, self._day.day))
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "network": self.network,
            "day": self.day,
            "age": self.age
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, title="", network=""):
        """only updates values with length"""
        if len(title) > 0:
            self.title = title
        if len(network) > 0:
            self.network = network
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initBreakingNews():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = BreakingNews(title='Bolsonaro supporters storm Brazilian Congress.', network='CNN', day=date(2023, 1, 21))
    u2 = BreakingNews(title='Kevin McCarthy is new speaker', network='Fox', day=date(2023, 1, 20))
    u3 = BreakingNews(title='Woman sentenced to three years in state prison for collecting 400,000 in viral GoFundMe scam', network='ABC', day=date(2023, 1, 19))
    u4 = BreakingNews(title='Ukraine denies Russian claim it killed 600 soldiers', network='NBC', day=date(2023, 1, 20))
    u5 = BreakingNews(title='Damar Hamlin: Buffalo Bills make stirring display in support of safety during victory', network='BBC', day=date(2023, 1, 22))
    u6 = BreakingNews(title='Worshippers in Tokyo plunge into ice bath to mark new year', network='CNN', day=date(2023, 1, 21))
    u7 = BreakingNews(title='Driver crashes and flips vehicle inside drive-through car wash', network='Fox', day=date(2023, 1, 20))
    u8 = BreakingNews(title='Brazilian police fire tear gas at Bolsonaro supporters', network='ABC', day=date(2023, 1, 19))
    u9 = BreakingNews(title='Deer rescued from frozen river in Wisconsin', network='NBC', day=date(2023, 1, 20))
    u10 = BreakingNews(title='Two years after Covid food still tastes rotten', network='BBC', day=date(2023, 1, 22))

    
    breaking_news = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10]
    # breaking_news = [u1, u2, u3, u4, u5]

    """Builds sample user/note(s) data"""
    for news in breaking_news:
        try:
            news.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {news.uid}")
            
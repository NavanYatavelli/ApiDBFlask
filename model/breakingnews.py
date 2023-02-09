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
    _city = db.Column(db.String(255), unique=False, nullable=False)
    _zip =  db.Column(db.Integer, primary_key=True, unique=False)
    _link = db.Column(db.String(1024), unique=False, nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, title, network, day=date.today(), city, zip, link):
        self._title = title    # variables with self prefix become part of the object, 
        self._network = network
        self._day = day
        self._city = city
        self._zip = zip
        self._link = link

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

    # a getter method, extracts city from object
    @property
    def city(self):
        return self._city
    
    # a setter function, allows city to be updated after initial object creation
    @network.setter
    def city(self, city):
        self._city = city
        
    # a getter method, extracts zip from object
    @property
    def zip(self):
        return self._zip
    
    # a setter function, allows zip to be updated after initial object creation
    @network.setter
    def zip(self, zip):
        self._zip = zip

    # a getter method, extracts link from object
    @property
    def link(self):
        return self._link
    
    # a setter function, allows link to be updated after initial object creation
    @network.setter
    def zip(self, link):
        self._link = link
        
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
            "age": self.age,
            "city": self.city,
            "zip": self.zip,
            "link": self.link
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
    u1 = BreakingNews(title='Padres FanFest mayhem: Long lines, crowded concourses, and delayed entry', network='CNN', day=date(2023, 1, 21), city="San Diego", zip=92127,"https://www.cbs8.com/article/news/local/padres-fanfest-mayhem-crowded-concourses-and-delayed-entry/509-543c588b-0eba-4c95-bb84-b3538894dd77")
    u2 = BreakingNews(title='Temecula - Forklifts Stolen From Home Depot', network='Fox', day=date(2023, 1, 20), city="Temecula", zip=92028,"https://fox5sandiego.com/news/local-news/forklift-stolen-from-oceanside-home-depot-in-broad-daylight/")
    u3 = BreakingNews(title='Long Beach State beats UC Irvine in OT', network='ABC', day=date(2023, 1, 19), city="Irvine", zip=92697,"https://www.usatoday.com/story/sports/ncaab/2023/02/05/long-beach-state-beats-uc-irvine-in-ot-for-6th-straight-win/51256357/")
    u4 = BreakingNews(title='El Centro will conduct a public hearing for new parks', network='NBC', day=date(2023, 1, 20), city="El Centro", zip=92243,"https://www.ivpressonline.com/")
    u5 = BreakingNews(title='Backpacking Permits For Joshua Tree National Park Available Online', network='BBC', day=date(2023, 1, 22), city="Joshua Tree", zip=92252,"https://www.nps.gov/jotr/planyourvisit/permitsandreservations.htm")
    u6 = BreakingNews(title='Escondido council appoints Palomar College trustee to vacant seat', network='CNN', day=date(2023, 1, 21), city="Escondido", zip=92025, "https://thecoastnews.com/escondido-council-appoints-palomar-college-trustee-to-vacant-seat/")
    u7 = BreakingNews(title='Salton Sea reduced inflow, the lake is shrinking and rising in salinity', network='Fox', day=date(2023, 1, 20), city="Salton Sea", zip=92274,"https://onlinelibrary.wiley.com/doi/10.1111/1752-1688.13063?af=R")
    u8 = BreakingNews(title='Mouse born at San Diego Zoo Safari Park wins Guinness award for longevity', network='CNN', day=date(2023, 1, 21), city="San Diego", zip=92127,"https://www.10news.com/news/local-news/mouse-born-at-san-diego-zoo-safari-park-wins-guinness-award-for-longevity")
    u9 = BreakingNews(title='Irvine Spectrum Adds First OC Shake Shack', network='NBC', day=date(2023, 1, 20), city="Irvine", zip=92697,"https://www.10news.com/news/local-news/mouse-born-at-san-diego-zoo-safari-park-wins-guinness-award-for-longevity")
    u10 = BreakingNews(title='San Diego celebrates National Pizza Day', network='BBC', day=date(2023, 1, 22), city="San Diego", zip=92127,"https://www.kusi.com/san-diego-celebrates-national-pizza-day/")

    
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
            

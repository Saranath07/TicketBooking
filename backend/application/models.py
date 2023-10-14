from .database import db
from datetime import datetime

class Users(db.Model):
   __tablename__ = "users"
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.String())
   name = db.Column(db.String(50), unique = True)
   password = db.Column(db.String(50))
   lastseen = db.Column(db.Float())
   email = db.Column(db.String())
   active = db.Column(db.Boolean())
   role = db.Column(db.String())
   user_bookings = db.relationship('Bookings', backref='user', cascade='all, delete')
   language = db.Column(db.String(50))
   region = db.Column(db.String(50))




class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer(), primary_key=True)
    venue_id = db.Column(db.String())
    venue_name = db.Column(db.String(50), unique = True)
    venue_description = db.Column(db.String())
    region = db.Column(db.String())
    capacity = db.Column(db.Integer())
    admin_id = db.Column(db.Integer(), db.ForeignKey(Users.id, ondelete='CASCADE'))
    showvenues = db.relationship('ShowVenue', cascade='all, delete')


class Shows(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer(), primary_key=True)
    show_id = db.Column(db.String())
    show_pic = db.Column(db.Text())
    show_description = db.Column(db.String())
    show_name = db.Column(db.String(50), unique = True)
    ratings = db.Column(db.Integer())
    tags = db.Column(db.String())
    language = db.Column(db.String())
    admin_id = db.Column(db.Integer(), db.ForeignKey(Users.id, ondelete='CASCADE'))
    venues = db.relationship('ShowVenue', cascade='all, delete')
    K = db.Column(db.Integer())
    

class ShowVenue(db.Model):
    __tablename__ = "showvenue"
    id = db.Column(db.Integer(), primary_key = True)
    showvenue_id = db.Column(db.String())
    show_id = db.Column(db.String(), db.ForeignKey(Shows.show_id, ondelete='CASCADE'))
    venue_id = db.Column(db.String(), db.ForeignKey(Venue.venue_id, ondelete='CASCADE'))
    available_seats = db.Column(db.Integer())
    price = db.Column(db.Float())
    timings = db.Column(db.String())
    bookings = db.relationship('Bookings', cascade='all, delete', passive_deletes=True)
    

class Bookings(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String())
    user_id = db.Column(db.String(), db.ForeignKey('users.id', ondelete='CASCADE'))
    showvenue_id = db.Column(db.String(), db.ForeignKey('showvenue.id', ondelete='CASCADE'))
    seat_number = db.Column(db.Integer(), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)



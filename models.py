from sqlalchemy import Column, String, Integer,Boolean
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String(100))
    seeking_talent=db.Column(db.Boolean)
    seeking_description=db.Column(db.String(450))
    #genres=db.relationship('VenueGenre',backref='venue',lazy=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    shows=db.relationship('Show',backref='venue',lazy='joined', cascade='all, delete')

    def insert_venue(self):
        db.session.add(self)
        db.session.commit()

    def format_venue(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres":self.genres,#[genre.genre for genre in self.genres],
            "address":self.address,
            "city": self.city,
            "state": self.state,
            "phone":self.phone,
            "website":self.website,
            "facebook_link":self.facebook_link,
            "seeking_talent":self.seeking_talent,
            "seeking_description":self.seeking_description,
            "image_link":self.image_link
        }


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String(100))
    seeking_venue=db.Column(db.Boolean)
    seeking_description=db.Column(db.String(450))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    shows=db.relationship('Show',backref='artist',lazy=True)


    def insert_artist(self):                   
        db.session.add(self)
        db.session.commit()



    def format_artist(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres":self.genres,#[genre.genre for genre in self.genres],
            "city": self.city,
            "state": self.state,
            "phone":self.phone,
            "website":self.website,
            "facebook_link":self.facebook_link,
            "seeking_venue":self.seeking_venue,
            "seeking_description":self.seeking_description,
            "image_link":self.image_link
        }


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
  __tablename__='shows'

  id=db.Column(db.Integer,primary_key=True)
  artist_id=db.Column(db.Integer,db.ForeignKey('artists.id'),nullable=False)
  venue_id=db.Column(db.Integer,db.ForeignKey('venues.id'),nullable=False)
  start_time=db.Column(db.DateTime)

  def format_show_venue(self):
    return {
            'artist_id':self.artist_id,
            'artist_name':self.artist.name,
            'artist_image_link':self.artist.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }

  def format_show_artist(self):
    return {
            'venue_id':self.venue_id,
            'venue_name':self.venue.name,
            'venue_image_link':self.venue.image_link,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }

  def format_show(self):
    return {    
          'venue_id': self.venue_id,
          'venue_name': self.venue.name,
          'artist_id': self.artist_id,
          'artist_name': self.artist.name,
          'artist_image_link': self.artist.image_link,
          'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }


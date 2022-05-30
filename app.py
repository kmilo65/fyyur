#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from requests import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, CsrfProtect
from forms import *
import config
from models import Venue,Artist,Show,db
from flask_migrate import Migrate
from datetime import date
import sys



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.secret_key=config.SECRET_KEY
csrf=CsrfProtect(app)
#db = SQLAlchemy(app)
db.init_app(app)  # <-- just init it
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  cities=[]
  for city in [{'city':venue.city ,'state': venue.state} for venue in Venue.query.order_by(Venue.city).all()]:
    if city not in cities:
      cities.append(city)

  data=[]
  for city in cities:
      venues=[{'id':venue.id,'name':venue.name} for venue in Venue.query.all() if venue.city==city['city'] and venue.state==city['state']]
      data.append({'city':city['city'],'state':city['state'],'venues':venues} )

  print(data)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form['search_term']
  search_result = Venue.query.order_by(Venue.id).filter(Venue.name.ilike('%{}%'.format(search_term))).order_by(Show.start_time).all() 
  count=len(search_result)
 
  data=[{'id':venue.id,
        'name':venue.name,
         'num_upcoming_shows':len(db.session.query(Show).filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).order_by(Show.start_time).all())}
        for venue in search_result ]

  response={
    'count':count,
    'data' : data
   }

  print(data)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue=Venue.query.get(venue_id)
  formatted_venue=Venue.format_venue(venue)
  
  # past shows
  """
  past_shows=[Show.format_show_venue(show) for show in
                  Show.query.filter(Show.venue_id==venue_id,Show.start_time<datetime.now()).order_by(Show.start_time).all()] 
  """
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).order_by(Show.start_time).all()   
  past_shows = []
  for show in past_shows_query:
      past_shows.append(Show.format_show_venue(show))
  past_shows_count=len(past_shows)
 

  # upcoming shows
  """
  upcoming_shows=[Show.format_show_venue(show) for show in 
                    Show.query.filter(Show.venue_id==venue_id,Show.start_time>=datetime.now()).order_by(Show.start_time).all()] 
  """
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime.now()).order_by(Show.start_time).all()   
  upcoming_shows = []
  for show in upcoming_shows_query:
      upcoming_shows.append(Show.format_show_venue(show))
  upcoming_shows_count=len(upcoming_shows)

  formatted_venue['past_shows']=past_shows
  formatted_venue['upcoming_shows']=upcoming_shows
  formatted_venue['past_shows_count']=past_shows_count
  formatted_venue['upcoming_shows_count']=upcoming_shows_count

  print(formatted_venue)

  return render_template('pages/show_venue.html', venue=formatted_venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion 
  form=VenueForm(request.form)

  try:

    if form.validate_on_submit():
      
        venue=Venue( name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data,
                    website=form.website_link.data,
                    seeking_talent=form.seeking_talent.data,
                    seeking_description=form.seeking_description.data,
                    genres = form.genres.data)
        Venue.insert_venue(venue)
        #on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!','success')

    else:
        for field, message in form.errors.items():
            flash(field + ' - ' + str(message))
 
  
  except:
  #    # TODO: on unsuccessful db insert, flash an error instead.
  #    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  #    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
       db.session.rollback()
       print(sys.exc_info())
       flash('An error occurred. Venue ' +request.form['name']  + ' could not be listed...please try again','error')
       return redirect(url_for('create_venue_form')) 
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/delete', methods=['GET','DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  print(request.args.get('methods'))
  print(request.get_data)
  if request.method=='DELETE':
    try:
        Show.query.filter_by(venue_id=venue_id).delete()
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue id {} was successfully deleted...!'.format(venue_id),'success')
        return redirect(url_for('index'))
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred deleting Venue id {}...please try again'.format(venue_id),'error')
    finally:
      db.session.close()
    # return None
    return redirect(url_for('venues'))

  if request.method=='GET':
    try:
        Show.query.filter_by(venue_id=venue_id).delete()
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue id {} was successfully deleted...!'.format(venue_id),'success')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred deleting Venue id {}...please try again'.format(venue_id),'error')
    finally:
      db.session.close()
    return redirect(url_for('venues'))

  


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists=Artist.query.order_by(Artist.name).all()
  data=[{'id':artist.id,'name':artist.name} for artist in artists]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form['search_term']
  search_result = Artist.query.order_by(Artist.id).filter(Artist.name.ilike('%{}%'.format(search_term))).all() 
  count=len(search_result)
 
  data=[{'id':artist.id,
        'name':artist.name,
         'num_upcoming_shows':len(db.session.query(Show).filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all())}
        for artist in search_result ]

  response={
    'count':count,
    'data' : data
   }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist=Artist.query.get(artist_id)
  formatted_artist=artist.format_artist()
  print(formatted_artist)

  # past shows
  """
  past_shows=Show.query.filter(Show.artist_id==artist_id,Show.start_time<datetime.now()).all()
  past_shows=[Show.format_show_artist(show) for show in past_shows]
  """
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).order_by(Show.start_time).all()   
  past_shows = []
  for show in past_shows_query:
      past_shows.append(Show.format_show_artist(show))
  past_shows_count=len(past_shows)

  # upcoming shows
  """
  upcoming_shows=Show.query.filter(Show.artist_id==artist_id,Show.start_time>=datetime.now()).all()
  upcoming_shows=[Show.format_show_artist(show) for show in upcoming_shows]
  """
  upcoming_shows_query=db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime.now()).order_by(Show.start_time).all()
  upcoming_shows=[]
  for show in upcoming_shows_query:
      upcoming_shows.append(Show.format_show_artist(show))
  upcoming_shows_count=len(upcoming_shows)

  formatted_artist['past_shows']=past_shows
  formatted_artist['upcoming_shows']=upcoming_shows
  formatted_artist['past_shows_count']=past_shows_count
  formatted_artist['upcoming_shows_count']=upcoming_shows_count

  return render_template('pages/show_artist.html', artist=formatted_artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get_or_404(artist_id)
  print("artist")
  print(artist.genres[0])
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form=ArtistForm(request.form)
  db.session().query(Artist).filter(
        Artist.id==artist_id
        ).update(
          {
            Artist.name:form.name.data,
            Artist.city:form.city.data,
            Artist.state:form.state.data,
            Artist.phone:form.phone.data,
            Artist.genres:form.genres.data,
            Artist.image_link:form.image_link.data,
            Artist.website:form.website_link.data,
            Artist.seeking_venue:form.seeking_venue.data,
            Artist.seeking_description:form.seeking_description.data
          }
        )
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  venue=Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form=VenueForm(request.form)
  db.session.query(Venue).filter(
        Venue.id==venue_id
        ).update(
        {
          Venue.name:form.name.data,
          Venue.city:form.city.data,
          Venue.state:form.state.data,
          Venue.address:form.address.data,
          Venue.phone:form.phone.data,
          Venue.image_link:form.image_link.data,
          Venue.facebook_link:form.facebook_link.data,
          Venue.website:form.website_link.data,
          Venue.seeking_talent:form.seeking_talent.data,
          Venue.seeking_description:form.seeking_description.data,
          Venue.genres : form.genres.data 
        })
  
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)

  try:
    if form.validate_on_submit():
      artist=Artist( name=form.name.data,
                      city=form.city.data,
                      state=form.state.data,
                      phone=form.phone.data,
                      genres=form.genres.data,
                      facebook_link=form.facebook_link.data,
                      image_link=form.image_link.data,
                      website=form.website_link.data,
                      seeking_venue=form.seeking_venue.data,
                      seeking_description=form.seeking_description.data)

      Artist.insert_artist(artist)
        # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!','success')
    else:
          for field, message in form.errors.items():
            flash(field + ' - ' + str(message))
  
  except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' +request.form['name'] + ' could not be listed....please try again!!','error')
      return redirect(url_for('create_artist_form'))

  finally:
     db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows=Show.query.order_by(db.desc(Show.start_time)).all()
  formatted_show=[Show.format_show(show) for show in shows]  
  return render_template('pages/shows.html', shows=formatted_show)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
 
  form=ShowForm(request.form)
  try:
      show=Show( venue_id=form.venue_id.data,
                 artist_id=form.artist_id.data,
                 start_time=form.start_time.data)

      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!','success')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed...Please try again')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      print(sys.exc_info())
      flash(u'An error occurred. Show could not be listed......Please try again!!', 'error')
      return redirect(url_for('create_shows'))

  # on successful db insert, flash success
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

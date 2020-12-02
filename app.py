#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
from datetime import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#import flask migrate
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#migrate instantiation
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database ||--COMPLETE--||

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# ---------------  Venue Genre Table -----------------------------------------------
venue_genre = db.Table('venue_genre',
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)
# ---------------  Artist Genre Table -----------------------------------------------
artist_genre = db.Table('artist_genre',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)
# ------------------  Genre Table (Association Object) --------------------------------------------------------
class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    
    artists = db.relationship('Artist', secondary=artist_genre, backref=db.backref('genres', lazy='dynamic'))
    venues = db.relationship('Venue', secondary=venue_genre, backref=db.backref('genres', lazy='dynamic'))
# ------------------  Show Table  --------------------------------------------------------
class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, primary_key=True)
    
    artist = db.relationship('Artist', backref=db.backref("shows"))
    venue = db.relationship('Venue', backref=db.backref('shows'))
# ------------------  Venue Table  --------------------------------------------------------
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False) 
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    # new 
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    artist = db.relationship('Show', back_populates='venue')
# ------------------  Artist Table  --------------------------------------------------------
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    # genres = db.Column(db.String(120)) || removed (will create table for this) ||
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    # new 
    website = db.Column(db.String, nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    venues = db.relationship('Show', back_populates='artist')
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  #------------------------------------------------------------------------------#
  # This makes sure genre table has the right data because it is being referenced
  #------------------------------------------------------------------------------#
  # Delete all data from genre table
  try:
    db.session.query(Genre).delete()
    db.session.commit()
    alternative = Genre(name='Alternative')
    blues = Genre(name='Blues')
    classical = Genre(name='Classical')
    country = Genre(name='Country')
    electronic = Genre(name='Electronic')
    folk = Genre(name='Folk')
    funk = Genre(name='Funk')
    hipHop = Genre(name='Hip-Hop')
    heavyMetal = Genre(name='Heavy Metal')
    instrumental = Genre(name='Instrumental')
    jazz = Genre(name='Jazz')
    musicalTheatre = Genre(name='Musical Theatre')
    pop = Genre(name='Pop')
    punk = Genre(name='Punk')
    rAndB = Genre(name='R&B')
    Reggae = Genre(name='Reggae')
    rockNRoll = Genre(name='Rock n Roll')
    soul = Genre(name='Soul')
    other = Genre(name='Other')
    db.session.add(alternative)
    db.session.add(blues)
    db.session.add(classical)
    db.session.add(country)
    db.session.add(electronic)
    db.session.add(folk)
    db.session.add(funk)
    db.session.add(hipHop)
    db.session.add(heavyMetal)
    db.session.add(instrumental)
    db.session.add(jazz)
    db.session.add(musicalTheatre)
    db.session.add(pop)
    db.session.add(punk)
    db.session.add(rAndB)
    db.session.add(Reggae)
    db.session.add(rockNRoll)
    db.session.add(soul)
    db.session.add(other)
    db.session.commit()
  except:
    db.session.rollback()
    print('Table already exist and may be referenced')
  # Insert data into genre table

  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #get all cities
  all_cities = []
  cities = []
  city_venues = []
  try:
    venues = Venue.query.all()
    for venue in venues:
          if (venue.city + ', ' + venue.state) not in all_cities:
                all_cities.append(venue.city + ', ' + venue.state)
                city_venues = Venue.query.filter_by(city=venue.city).all()
                venue_list = []
                for venue in city_venues:
                      venue_list.append({
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": 0
                      })
                cities.append(
                  {
                    "city": venue.city,
                    "state": venue.state,
                    "venues": venue_list
                  }
                )
    data = cities
  except:
    print(sys.exc_info())
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  print(search_term)
  # get venues
  venues = []
  result = []
  try:
    venues = Venue.query.all()
    for venue in venues:
          if search_term.lower() in venue.name.lower():
                result.append(
                  {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": 0
                  }
                )
  except:
    print(sys.exc_info())
  print(result)
  response={
    "count": len(result),
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = []
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    genres = []
    shows = venue.shows
    now = datetime.now()
    #
    past_shows = list(filter(lambda show: show.start_time < now, shows))
    past_shows_format = []
    for show in past_shows:
      print(venue.image_link)
      past_shows_format.append({
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
          "start_time": str(show.start_time)
      })
    past_shows_count = len(past_shows)
    upcoming_shows = list(filter(lambda show: show.start_time > now, shows))
    upcoming_shows_format = []

    for show in upcoming_shows: 
      upcoming_shows_format.append({
          "artist_id": show.artist_id,
          "artist_name": Artist.query.filter_by(id=show.venue_id).first().name,
          "artist_image_link": Artist.query.filter_by(id=show.venue_id).first().image_link,
          "start_time": str(show.start_time)
      })
    upcoming_shows_count = len(upcoming_shows)
    #
    for genre in venue.genres:
          genres.append(genre.name)
    data={
      "id": venue.id,
      "name": venue.name,
      "genres": genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows_format,
      "upcoming_shows": upcoming_shows_format,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
    }
  except:
    print(sys.exc_info())
    flash('Venue with id: ' + str(venue_id) + ' does not exist')
    return render_template('errors/500.html')

  return render_template('pages/show_venue.html', venue=data)

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
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  seeking_description = request.form.get('seeking_description')
  if (request.form.get('seeking_talent') == 'no'):
        seeking_talent = False
  else:
        seeking_talent = True
  website_link = request.form.get('website_link')
  image_link = request.form.get('image_link')
  try:
    # create venue
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, facebook_link=facebook_link, seeking_description=seeking_description, seeking_talent=seeking_talent, website=website_link)
    # adds genres to venue
    for genre in genres:
          venue_genre_single = Genre.query.filter_by(name=genre).first()
          venue.genres.append(venue_genre_single)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # print to console
    # print('something', file=sys.stderr)
  except:
    db.session.rollback()
    # prints error
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  try:
    artists = Artist.query.all()
    for artist in artists:
          data.append({
            "id": artist.id,
            "name": artist.name
          })
    print('Succeeded in getting artist')
  except:
    print(sys.exc_info())
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  print(search_term)
  # get artists
  artists = []
  result = []
  try:
    artists = Artist.query.all()
    for artist in artists:
          if search_term.lower() in artist.name.lower():
                result.append(
                  {
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": 0
                  }
                )
  except:
    print(sys.exc_info())
  print(result)
  response={
    "count": len(result),
    "data": result
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = []
  try:
    print(artist_id)
    artist = Artist.query.filter_by(id=artist_id).first()
    genres = []
    shows = artist.shows
    now = datetime.now()
    past_shows = list(filter(lambda show: show.start_time < now, shows))
    past_shows_format = []
    for show in past_shows:
      past_shows_format.append({
          "venue_id": show.venue_id,
          "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
          "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
          "start_time": str(show.start_time)
      })
    past_shows_count = len(past_shows)
    upcoming_shows = list(filter(lambda show: show.start_time > now, shows))
    upcoming_shows_format = []
    for show in upcoming_shows: 
      upcoming_shows_format.append({
          "venue_id": show.venue_id,
          "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
          "venue_image_link": Venue.query.filter_by(id=show.venue_id).first().image_link,
          "start_time": str(show.start_time)
      })
    upcoming_shows_count = len(upcoming_shows)
    for genre in artist.genres.all():
          print(genre.name)
    data={
      "id": artist.id,
      "name": artist.name,
      "genres": genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_shows_format,
      "upcoming_shows": upcoming_shows_format,
      "past_shows_count": past_shows_count,
      "upcoming_shows_count": upcoming_shows_count,
    }
  except:
    print(sys.exc_info())
    flash('Artist with id: ' + str(artist_id) + ' does not exist')
    return render_template('errors/500.html')
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
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
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link')
  image_link = request.form.get('image_link')
  seeking_description = request.form.get('seeking_description')
  if (request.form.get('seeking_venue') == 'no'):
        seeking_venue = False
  else:
        seeking_venue = True
  website_link = request.form('website_link')
  # TODO: modify data to be the data object returned from db 
  try:
    artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, facebook_link=facebook_link, seeking_description=seeking_description, seeking_venue=seeking_venue, website=website_link)
    # add genres to artist
    for genre in genres:
          artist_genre = Genre.query.filter_by(name=genre).first()
          artist.genres.append(artist_genre)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    # prints error
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  try:
    shows = Show.query.all()
    for show in shows:
          data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_image_link": show.artist.image_link,
            "start_time": datetime.strftime(show.start_time, "%m/%d/%Y, %H:%M:%S")
          })
    print('Succeeded in appending shows')
  except:
    print(sys.exc_info())
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')
  # TODO: insert form data as a new Show record in the db, instead
  try:
    #checks if artist exist
    artist = Artist.query.filter_by(id=artist_id).first()
    venue = Venue.query.filter_by(id=venue_id).first()
    show = Show(start_time=start_time)
    show.artist_id = artist_id
    show.venue_id = venue_id
    db.session.add(show)
    db.session.commit()
    print('Artist: ' + artist.name)
    print('Venue: ' + venue.name)
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print('Something went wrong')
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    print('done')
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

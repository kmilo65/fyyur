"""empty message

Revision ID: 297040b0a36b
Revises: 
Create Date: 2022-04-10 16:15:51.320290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '297040b0a36b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=450), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=450), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artist_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=120), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=120), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    # Inserting vanues
    op.execute("insert into venues(id,name,city,state,address,phone,image_link,facebook_link,website,seeking_talent,seeking_description) values(1,'The Musical Hop','San Francisco','CA','1015 Folsom Street','123-123-1234','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60','https://www.facebook.com/TheMusicalHop','https://www.themusicalhop.com',True,'We are on the lookout for a local artist to play every two weeks. Please call us.');")
    op.execute("insert into venues(id,name,city,state,address,phone,image_link,facebook_link,website,seeking_talent,seeking_description) values(2,'The Dueling Pianos Bar','New York','NY','335 Delancey Street','914-003-1132', 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80','https://www.facebook.com/theduelingpianos', 'https://www.theduelingpianos.com',False,NULL);")
    op.execute("insert into venues(id,name,city,state,address,phone,image_link,facebook_link,website,seeking_talent,seeking_description) values(3,'Park Square Live Music & Coffee','San Francisco','CA','34 Whiskey Moore Ave','415-000-1234','https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80','https://www.facebook.com/ParkSquareLiveMusicAndCoffee','https://www.parksquarelivemusicandcoffee.com',False,NULL );")

    # Inserting artists
    op.execute("insert into artists(id,name,city,state,phone,image_link,facebook_link,website,seeking_venue,seeking_description) values(4,'Guns N Petals','San Francisco','CA','326-123-5000','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80','https://www.facebook.com/GunsNPetals','https://www.gunsnpetalsband.com',True,'Looking for shows to perform at in the San Francisco Bay Area!');")
    op.execute("insert into artists(id,name,city,state,phone,image_link,facebook_link,website,seeking_venue,seeking_description) values(5,'Matt Quevedo','New York','NY','300-400-5000','https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80','https://www.facebook.com/mattquevedo923251523',NULL,False,NULL);")
    op.execute("insert into artists(id,name,city,state,phone,image_link,facebook_link,website,seeking_venue,seeking_description) values(6,'The Wild Sax Band','San Francisco','CA','432-325-5432','https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',NULL,NULL,False,NULL);")

    # Inserting shows
    op.execute("insert into shows(id,artist_id,venue_id,start_time) values(1,4,1,'2019-05-21T21:30:00.000Z')")  
    op.execute("insert into shows(id,artist_id,venue_id,start_time) values(2,5,3,'2019-06-15T23:00:00.000Z')")  
    op.execute("insert into shows(id,artist_id,venue_id,start_time) values(3,6,3,'2035-04-01T20:00:00.000Z')")  
    op.execute("insert into shows(id,artist_id,venue_id,start_time) values(4,6,3,'2035-04-08T20:00:00.000Z')")  
    op.execute("insert into shows(id,artist_id,venue_id,start_time) values(5,6,3,'2035-04-15T20:00:00.000Z')")  

    # Inserting artist_genres
    op.execute("insert into artist_genres(id,genre,artist_id) values(1,'Rock n Roll',4);")
    op.execute("insert into artist_genres(id,genre,artist_id) values(2,'Jazz',5);")
    op.execute("insert into artist_genres(id,genre,artist_id) values(3,'Jazz',6);")
    op.execute("insert into artist_genres(id,genre,artist_id) values(4,'Classical',6);")

    # Inserting venu_genres
    op.execute("insert into venue_genres(id,genre,venue_id) values(1,'Jazz',1);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(2,'Reggae',1);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(3,'Swing',1);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(4,'Classical',1);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(5,'Folk',1);")

    op.execute("insert into venue_genres(id,genre,venue_id) values(6,'Classical',2);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(7,'R&B',2);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(8,'Hip-Hop',2);")

    op.execute("insert into venue_genres(id,genre,venue_id) values(9,'Rock n Roll',3);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(10,'Jazz',3);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(11,'Classical',3);")
    op.execute("insert into venue_genres(id,genre,venue_id) values(12,'Folk',3);")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genres')
    op.drop_table('shows')
    op.drop_table('artist_genres')
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###

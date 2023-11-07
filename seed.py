'''Seed file to make sample data for users db'''

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users and posts
johnny_depp=User(first_name='Johnny', last_name='Depp', image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Johnny_Depp-2757_%28cropped%29.jpg/1058px-Johnny_Depp-2757_%28cropped%29.jpg')

angelina_jolie=User(first_name='Angelina', last_name='Jolie', image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Under_Secretary_Zeya_Meets_With_UNHCR_Special_Envoy_Jolie_%2851942861677%29_%28cropped%29.jpg/440px-Under_Secretary_Zeya_Meets_With_UNHCR_Special_Envoy_Jolie_%2851942861677%29_%28cropped%29.jpg')

jolie_post_1=Post(title='Hello', content='I am greeting you', users=angelina_jolie)
jolie_post_2=Post(title='Hello again', content='I am greeting you the second time', users=angelina_jolie)

depp_post_1=Post(title='Bye-bye', content='Firewall!', users=johnny_depp)
depp_post_2=Post(title='Bye-bye again', content='Firewall my firend!', users=johnny_depp)

# Add new objects to session, so they'll persist
db.session.add(johnny_depp)
db.session.add(angelina_jolie)

db.session.commit()

db.session.add(jolie_post)
db.session.add(depp_post)

db.session.commit()
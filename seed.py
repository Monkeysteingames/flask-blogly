from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
zach = User(first_name='Zach', last_name='Augustine',
            img_url='https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/02/322868_1100-800x825.jpg')
melissa = User(first_name='Melissa', last_name='Augustine',
               img_url='https://post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/02/322868_1100-800x825.jpg')

# Add new objects to session, so they'll persist
db.session.add(zach)
db.session.add(melissa)


# Commit--otherwise, this never gets saved!
db.session.commit()

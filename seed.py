from models import User, db, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
zach = User(first_name='Zach', last_name='Augustine',
            img_url='https://thumbs.dreamstime.com/b/cute-boy-cartoon-illustration-90163697.jpg')
melissa = User(first_name='Melissa', last_name='Augustine',
               img_url='https://image.shutterstock.com/image-vector/happy-african-american-girl-cartoon-260nw-522003124.jpg')
buster = User(first_name='Buster', last_name='Augustine',
              img_url='https://cdn.mos.cms.futurecdn.net/VSy6kJDNq2pSXsCzb6cvYF.jpg')

db.session.add_all([zach, melissa, buster])
db.session.commit()

z_post1 = Post(title='First Post!',
               content='Content for First Post!', user_id=1)
z_post2 = Post(title='Second Post!',
               content='Content for Second Post!', user_id=1)
m_post1 = Post(title='My First Post!',
               content='Content for My First Post!', user_id=2)
m_post2 = Post(title='My Second Post!',
               content='Content for My Second Post!', user_id=2)
b_post1 = Post(title='MEOW',
               content='eck eck eck eck eck..(pause)...MEOWWWWWWWW!', user_id=3)

db.session.add_all([z_post1, z_post2, m_post1, m_post2, b_post1])
db.session.commit()

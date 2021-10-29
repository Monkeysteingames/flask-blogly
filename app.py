from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Catsareamazingcutecreatures21213'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home():
    """Shows homepage of our app"""
    return render_template('home.html')


@app.route('/users')
def show_users():
    """Show our list of all the users"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_new_user_form():
    """Show form to add new user to database"""
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """gather form data and create new user in database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form.get('img_url')

    new_user = User(first_name=first_name,
                    last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details about user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def change_user_details(user_id):
    """Edit the row/user in our database based on the form data retrieved"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form.get('img_url')

    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """remove user from database"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    users = User.query.all()
    # .rollback() - maybe add functionality to check if we're sure!
    return render_template('users.html', users=users)

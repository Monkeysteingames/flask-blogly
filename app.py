from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
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


############# User Routes #################

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
    posts = Post.query.all()
    return render_template('user_details.html', user=user, posts=posts)


@ app.route('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user, )


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

################ Post Routes ######################


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Display form to create a new post"""
    user_id = user_id
    return render_template('post_new.html', user_id=user_id)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user_id = user_id
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    # user = User.query.get_or_404(user_id)
    # posts = Post.query.all()
    # return render_template('user_details.html', user=user, posts=posts)
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    return render_template('post_details.html', post=post, user_id=user_id)


@app.route('/posts/<int:post_id>/edit')
def show_edit_form_for_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    return render_template('post_edit.html', post=post, user_id=user_id)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user_id}")

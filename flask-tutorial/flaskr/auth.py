import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, 
    request, session, url_for
)

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else: # else is executed if try does not raise any errors
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Should probably change this to just be incorrect username or password
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"


        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# This is a decorator to protect routes that require a 
# logged-in user.
def login_required(view):
    # This preserves the original function's metadata 
    # (like name, docstring)
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # 'g' is a special Flask object that stores data during a request.
        # Here we check if g.user is None (i.e., not logged in)
        if g.user is None:
            # If the user is not logged in, redirect them to the login page
            return redirect(url_for('auth.login'))
        # If the user is logged in, proceed with the original view function
        return view(**kwargs)
    # Return the new, wrapped version of the view function
    return wrapped_view
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User



bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if "user_id" not in session:
        return render_template ('index.html')
    else:
        return redirect('/dashboard')



@app.route('/register/', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid: # if isValid is False the redirect back to '/' with flash message
        return redirect('/')
    else:
        newUser = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(newUser)
        if not id:
            flash("Something got messed up someplace")
            return redirect('/')
        else:
            session['user_id'] = id
            flash("You logged in")
            return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # user = User.getEmail(request.form)
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data)
    print(user)
    if not user:
        print("not user if triggered")
        flash("No email in data base, please register.")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        print("not password if triggered")
        flash("Wrong Password")
        return redirect('/')
    session['user_id'] = user.id
    flash("Welcome back")
    return redirect('/dashboard')

@app.route('/login_page')
def login_page():
    if "user_id" not in session:
        return render_template ('login_page.html')
    else:
        return redirect('/dashboard')
    

@app.route('/sales_inventory')
def sales_inventory():
        return render_template('sales_inventory.html')


@app.route('/logout/')
def logout():
    session.clear()
    flash("Good Bye!")
    return redirect('/')

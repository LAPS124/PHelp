from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.job import Job
from flask_app.models.user import User
from flask_app.models.inventory import Product

#dashboard 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user_data={
            "id":id
        }
        theUser = User.getOne(data)
        job= Job.get_all()
        seller = Job.get_sales(user_data)
        return render_template('dashboard.html', user=theUser, jobs=job, sellers=seller)

    # return render_template("dashboard.html")

#new
@app.route('/proposal')
def proposal():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":session['user_id']
        }
    return render_template('proposal.html', user=User.getOne(data), stuff=Product.get_all_product())
#create
@app.route('/create/job/', methods= ['POST'])
def create_job():
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Job.validate_sales(request.form):
        return redirect ('/proposal')
    data = {
        "customer":request.form["customer"],
        "location":request.form["location"],
        "needed_by":request.form["needed_by"],
        "item":request.form['item'],
        "scope":request.form["scope"],
        "user_id":session["user_id"]
    }
    Job.save(data)
    print(Job)
    return redirect('/dashboard')
#edit
@app.route('/edit/job/<int:id>')
def edit_job(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" :session['user_id']
    }
    return render_template("edit.html", edit=Job.get_one(data), user=User.getOne(user_data))
#update
@app.route('/update/job', methods=["POST"])
def update_job():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_sales(request.form):
        return redirect('/new/job/')
    data = {
        "customer":request.form['customer'],
        "location":request.form["location"],
        "needed_by":request.form["needed_by"],
        "item":request.form["item"],
        "scope":request.form["scope"],
        "id":request.form["id"],
        "user_id":session["user_id"]
        }
    Job.update(data)
    return redirect('/dashboard')
#view
@app.route('/view/<int:id>')
def view_job(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id": session['user_id']
    }
    sales = Job.get_sales(data)
    return render_template('view_job.html', job=Job.get_one(data), user=User.getOne(user_data), sellers=sales)
#destroy
@app.route('/destroy/<int:id>')
def destroy_job(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Job.delete(data)
    print(data)
    return redirect('/dashboard')

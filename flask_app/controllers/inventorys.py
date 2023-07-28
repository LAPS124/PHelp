from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.job import Job
from flask_app.models.user import User
from flask_app.models.inventory import Product

@app.route('/inventory')
def proposal():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":session['user_id']
        }
    return render_template('sales_inventory.html', user=User.getOne(data))
#create
@app.route('/create/product/', methods= ['POST'])
def create_product():
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Product.validate_products(request.form):
        return redirect ('/new/product')
    data = {
        "product_name":request.form["product_name"],
        "part_number":request.form["part_number"],
        "product_info":request.form["product_info"],
        "price":request.form['price'],
        "install_time":request.form["install_time"],
        "starting_inventory":request.form["starting_inventory"],
        "inventory_on_hand":request.form["inventory_on_hand"],
        "inventory_needed":request.form["inventory_needed"],
        "user_id":session["user_id"]
    }
    Product.save(data)
    print(Product)
    return redirect('/inventory')
#edit
@app.route('/edit/product/<int:id>')
def edit_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" :session['user_id']
    }
    return render_template("edit_inventory.html", edit_item=Product.get_one(data), user=User.getOne(user_data))
#update
@app.route('/update/product', methods=["POST"])
def update_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_sales(request.form):
        return redirect('/new/product/')
    data = {
        "product_name":request.form["product_name"],
        "part_number":request.form["part_number"],
        "product_info":request.form["product_info"],
        "price":request.form['price'],
        "install_time":request.form["install_time"],
        "starting_inventory":request.form["starting_inventory"],
        "inventory_on_hand":request.form["inventory_on_hand"],
        "inventory_needed":request.form["inventory_needed"],
        "user_id":session["user_id"]
    }
    Product.update(data)
    return redirect('/inventory')
#view
@app.route('/view_product/<int:id>')
def view_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id": session['user_id']
    }
    product = Product.get_products(data)
    return render_template('inventory.html', products=Product.get_one_product(data), user=User.getOne(user_data), inventory=product)
#destroy
@app.route('/destroy_product/<int:id>')
def destroy_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Product.delete(data)
    print(data)
    return redirect('/inventory')

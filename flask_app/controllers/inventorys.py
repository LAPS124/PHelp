from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.job import Job
from flask_app.models.user import User
from flask_app.models.inventory import Product

@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {
            "id":id
        }
        user_data = {
            "id" :session['user_id']
        }
        daUser = User.getOne(data)
        product = Product.get_all_product()
        salesperson = Job.get_sales(user_data)

    return render_template("sales_inventory.html",  user= daUser, products=product, sales=salesperson)
@app.route('/newinventory')
def newinventory():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":session['user_id']
    }
    return render_template('new_inventory.html', user=User.getOne(data))
#create
@app.route('/create_product/', methods= ['POST'])
def create_product():
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Product.validate_products(request.form):
        return redirect ('/newinventory')
    data = {
        "product_name":request.form["product_name"],
        "part_number":request.form["part_number"],
        "product_info":request.form["product_info"],
        "price":request.form['price'],
        "install_time":request.form["install_time"],
        "inventory_on_hand":request.form["inventory_on_hand"],
        "inventory_needed":request.form["inventory_needed"],
        "user_id":session["user_id"]
    }
    Product.save_product(data)
    print(Product)
    return redirect('/inventory')
#edit
@app.route('/edit_product/<int:id>')
def edit_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" :session['user_id']
    }
    return render_template("edit_inventory.html", edit_product=Product.get_one_product(data), user=User.getOne(user_data))
#update
@app.route('/update/product', methods=["POST"])
def update_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_products(request.form):
        return redirect('/newinventory/')
    data = {
        "product_name":request.form["product_name"],
        "part_number":request.form["part_number"],
        "product_info":request.form["product_info"],
        "price":request.form['price'],
        "install_time":request.form["install_time"],
        "inventory_on_hand":request.form["inventory_on_hand"],
        "inventory_needed":request.form["inventory_needed"],
        "user_id":session["user_id"]
    }
    Product.update_product(data)
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
    return render_template('view_product.html', product=Product.get_one_product(data), user=User.getOne(user_data), inventory=product)
#destroy
@app.route('/destroy_product/<int:id>')
def destroy_product(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Product.delete_product(data)
    print(data)
    return redirect('/inventory')

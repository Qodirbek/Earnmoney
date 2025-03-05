from flask import Blueprint, render_template, request, redirect, url_for, flash
import json

admin = Blueprint('admin', __name__)

ORDERS_FILE = "app/orders.json"

def load_orders():
    try:
        with open(ORDERS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)

@admin.route('/dashboard')
def admin_dashboard():
    orders = load_orders()
    return render_template("admin.html", orders=orders)

@admin.route('/update_order', methods=['POST'])
def update_order():
    order_id = request.form.get("order_id")
    status = request.form.get("status")

    orders = load_orders()
    for order in orders:
        if order["id"] == order_id:
            order["status"] = status
            break

    save_orders(orders)
    flash("Buyurtma yangilandi!", "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/delete_order/<order_id>', methods=['GET'])
def delete_order(order_id):
    orders = load_orders()
    orders = [order for order in orders if order["id"] != order_id]

    save_orders(orders)
    flash("Buyurtma o‘chirildi!", "danger")
    return redirect(url_for('admin.admin_dashboard'))
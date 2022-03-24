from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('customer', __name__)


@bp.route('/customer')
def customer():
	if current_user.is_authenticated:
		recommended_products = ['abc']
		return render_template('customer.html', rec_prod = recommended_products)
	else:
		return redirect(url_for('index.index'))


@bp.route('/customer/account')
def customer_portal():
	if current_user.is_authenticated:
		return render_template('customer_portal.html')
	else:
		return redirect(url_for('index.index'))


@bp.route('/customer/account/my-cart')
def my_cart():
	msg = "Hello world!"
	return render_template('customer_my_cart.html', info = msg)


@bp.route('/customer/account/my-orders')
def my_orders():
	msg = "Hello world!"
	return render_template('customer_my_orders.html', info = msg)


@bp.route('/customer/account/my-profile')
def my_profile():
	msg = "Hello world!"
	return render_template('customer_my_profile.html', info = msg)


@bp.route('/customer/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('customer_my_messages.html', info = msg)


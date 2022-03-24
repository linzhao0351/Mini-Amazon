from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('seller', __name__)


@bp.route('/seller/account')
def seller_portal():
	if current_user.is_authenticated:
		return render_template('seller_portal.html')
	else:
		return redirect(url_for('index.index'))


@bp.route('/seller/account/my-profile')
def my_profile():
	msg = "Hello world!"
	return render_template('seller_my_profile.html', info = msg)


@bp.route('/seller/account/my-balance')
def my_balance():
	msg = "Hello world!"
	return render_template('seller_my_balance.html', info = msg)


@bp.route('/seller/account/my-inventory')
def my_inventory():
	msg = "Hello world!"
	return render_template('seller_my_inventory.html', info = msg)


@bp.route('/seller/account/my-orders')
def my_orders():
	msg = "Hello world!"
	return render_template('seller_my_orders.html', info = msg)


@bp.route('/seller/account/my-reviews')
def my_reviews():
	msg = "Hello world!"
	return render_template('seller_my_reviews.html', info = msg)


@bp.route('/seller/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('seller_my_messages.html', info = msg)